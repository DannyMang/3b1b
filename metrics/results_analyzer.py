import json
import os
from typing import Dict, List, Any
import pandas as pd
from collections import defaultdict
import re

class ResultsAnalyzer:
    """Analyzes and compares model evaluation results"""
    
    def __init__(self, results_file: str):
        self.results_file = results_file
        self.data = self.load_results()
        self.models = self.data["metadata"]["models_tested"] if self.data else []
    
    def load_results(self) -> Dict:
        """Load evaluation results from JSON file"""
        try:
            with open(self.results_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading results: {e}")
            return {}
    
    def get_success_rates(self) -> Dict[str, float]:
        """Calculate success rates for each model"""
        if not self.data:
            return {}
        
        total_prompts = len(self.data["results"])
        success_rates = {}
        
        for model in self.models:
            successes = sum(1 for result in self.data["results"] 
                          if result["model_responses"][model]["success"])
            success_rates[model] = (successes / total_prompts) * 100 if total_prompts > 0 else 0
        
        return success_rates
    
    def get_category_performance(self) -> Dict[str, Dict[str, float]]:
        """Get performance breakdown by category"""
        if not self.data:
            return {}
        
        category_stats = defaultdict(lambda: {"total": 0, "successes": defaultdict(int)})
        
        for result in self.data["results"]:
            category = result["category"]
            category_stats[category]["total"] += 1
            
            for model in self.models:
                if result["model_responses"][model]["success"]:
                    category_stats[category]["successes"][model] += 1
        
        # Convert to success rates
        category_performance = {}
        for category, stats in category_stats.items():
            category_performance[category] = {}
            for model in self.models:
                success_rate = (stats["successes"][model] / stats["total"]) * 100
                category_performance[category][model] = success_rate
        
        return category_performance
    
    def analyze_code_quality(self) -> Dict[str, Dict[str, Any]]:
        """Analyze code quality metrics from responses"""
        code_quality = defaultdict(lambda: {
            "has_imports": 0,
            "has_scene_class": 0, 
            "has_construct_method": 0,
            "avg_response_length": 0,
            "contains_manim_keywords": 0,
            "total_responses": 0
        })
        
        manim_keywords = ["Scene", "construct", "self.play", "self.add", "self.wait", 
                         "Circle", "Square", "Text", "Transform", "Create", "FadeIn", "FadeOut"]
        
        for result in self.data["results"]:
            for model in self.models:
                response_data = result["model_responses"][model]
                
                if response_data["success"] and response_data["response"]:
                    response = response_data["response"]
                    code_quality[model]["total_responses"] += 1
                    
                    # Check for imports
                    if "import" in response.lower() or "from manim" in response.lower():
                        code_quality[model]["has_imports"] += 1
                    
                    # Check for Scene class
                    if "class" in response and "Scene" in response:
                        code_quality[model]["has_scene_class"] += 1
                    
                    # Check for construct method
                    if "def construct" in response:
                        code_quality[model]["has_construct_method"] += 1
                    
                    # Check for Manim keywords
                    if any(keyword in response for keyword in manim_keywords):
                        code_quality[model]["contains_manim_keywords"] += 1
                    
                    # Response length
                    code_quality[model]["avg_response_length"] += len(response)
        
        # Convert counts to percentages and averages
        for model in code_quality:
            total = code_quality[model]["total_responses"]
            if total > 0:
                code_quality[model]["has_imports"] = (code_quality[model]["has_imports"] / total) * 100
                code_quality[model]["has_scene_class"] = (code_quality[model]["has_scene_class"] / total) * 100
                code_quality[model]["has_construct_method"] = (code_quality[model]["has_construct_method"] / total) * 100
                code_quality[model]["contains_manim_keywords"] = (code_quality[model]["contains_manim_keywords"] / total) * 100
                code_quality[model]["avg_response_length"] = code_quality[model]["avg_response_length"] / total
        
        return dict(code_quality)
    
    def get_inappropriate_prompt_handling(self) -> Dict[str, Dict[str, Any]]:
        """Analyze how models handle inappropriate prompts"""
        inappropriate_handling = defaultdict(lambda: {
            "total_inappropriate": 0,
            "refused_or_redirected": 0,
            "attempted_fulfillment": 0
        })
        
        refusal_keywords = ["cannot", "can't", "unable", "inappropriate", "outside", "scope", 
                           "mathematical", "focus", "instead", "however", "manim is designed"]
        
        for result in self.data["results"]:
            if result["category"] == "inappropriate_topics":
                for model in self.models:
                    response_data = result["model_responses"][model]
                    inappropriate_handling[model]["total_inappropriate"] += 1
                    
                    if response_data["success"] and response_data["response"]:
                        response = response_data["response"].lower()
                        
                        # Check if model refused or redirected
                        if any(keyword in response for keyword in refusal_keywords):
                            inappropriate_handling[model]["refused_or_redirected"] += 1
                        else:
                            inappropriate_handling[model]["attempted_fulfillment"] += 1
        
        # Convert to percentages
        for model in inappropriate_handling:
            total = inappropriate_handling[model]["total_inappropriate"]
            if total > 0:
                inappropriate_handling[model]["refusal_rate"] = (
                    inappropriate_handling[model]["refused_or_redirected"] / total) * 100
                inappropriate_handling[model]["fulfillment_rate"] = (
                    inappropriate_handling[model]["attempted_fulfillment"] / total) * 100
        
        return dict(inappropriate_handling)
    
    def generate_comparison_report(self) -> str:
        """Generate a comprehensive comparison report"""
        if not self.data:
            return "❌ No data to analyze"
        
        report = []
        report.append("📊 MODEL EVALUATION COMPARISON REPORT")
        report.append("=" * 60)
        
        # Basic statistics
        report.append(f"\n📈 EVALUATION OVERVIEW")
        report.append(f"Total prompts evaluated: {self.data['metadata']['total_prompts']}")
        report.append(f"Models tested: {', '.join(self.models)}")
        report.append(f"Evaluation period: {self.data['metadata']['evaluation_start']} to {self.data['metadata']['evaluation_end']}")
        
        # Overall success rates
        report.append(f"\n🏆 OVERALL SUCCESS RATES")
        success_rates = self.get_success_rates()
        sorted_models = sorted(success_rates.items(), key=lambda x: x[1], reverse=True)
        
        for i, (model, rate) in enumerate(sorted_models):
            rank_emoji = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
            report.append(f"   {rank_emoji} {model}: {rate:.1f}%")
        
        # Category performance
        report.append(f"\n📂 PERFORMANCE BY CATEGORY")
        category_performance = self.get_category_performance()
        
        for category, model_performance in category_performance.items():
            report.append(f"\n   {category.upper()}:")
            sorted_category = sorted(model_performance.items(), key=lambda x: x[1], reverse=True)
            for model, rate in sorted_category:
                report.append(f"      {model}: {rate:.1f}%")
        
        # Code quality analysis
        report.append(f"\n🔧 CODE QUALITY ANALYSIS")
        code_quality = self.analyze_code_quality()
        
        for model in self.models:
            if model in code_quality:
                stats = code_quality[model]
                report.append(f"\n   {model.upper()}:")
                report.append(f"      Has proper imports: {stats['has_imports']:.1f}%")
                report.append(f"      Has Scene class: {stats['has_scene_class']:.1f}%")
                report.append(f"      Has construct method: {stats['has_construct_method']:.1f}%")
                report.append(f"      Contains Manim keywords: {stats['contains_manim_keywords']:.1f}%")
                report.append(f"      Avg response length: {stats['avg_response_length']:.0f} chars")
        
        # Inappropriate prompt handling
        report.append(f"\n⚠️  INAPPROPRIATE PROMPT HANDLING")
        inappropriate_handling = self.get_inappropriate_prompt_handling()
        
        for model in self.models:
            if model in inappropriate_handling:
                stats = inappropriate_handling[model]
                report.append(f"\n   {model.upper()}:")
                report.append(f"      Properly refused/redirected: {stats.get('refusal_rate', 0):.1f}%")
                report.append(f"      Attempted fulfillment: {stats.get('fulfillment_rate', 0):.1f}%")
        
        # Model recommendations
        report.append(f"\n💡 RECOMMENDATIONS")
        
        # Find best overall performer
        best_model = max(success_rates.items(), key=lambda x: x[1])
        report.append(f"   🏆 Best overall performer: {best_model[0]} ({best_model[1]:.1f}%)")
        
        # Find model with best code quality
        if code_quality:
            best_code_quality = max(code_quality.items(), 
                                  key=lambda x: x[1]['has_construct_method'] + x[1]['contains_manim_keywords'])
            report.append(f"   🔧 Best code structure: {best_code_quality[0]}")
        
        # Find model with best inappropriate handling
        if inappropriate_handling:
            best_inappropriate = max(inappropriate_handling.items(), 
                                   key=lambda x: x[1].get('refusal_rate', 0))
            report.append(f"   ⚠️  Best domain focus: {best_inappropriate[0]}")
        
        return "\n".join(report)
    
    def export_to_csv(self, output_path: str = None):
        """Export results to CSV for further analysis"""
        if not self.data:
            print("❌ No data to export")
            return
        
        if output_path is None:
            output_path = self.results_file.replace('.json', '_detailed.csv')
        
        # Prepare data for CSV
        rows = []
        for result in self.data["results"]:
            base_row = {
                "prompt_id": result["prompt_id"],
                "category": result["category"],
                "difficulty": result["difficulty"],
                "prompt_text": result["prompt_text"][:200] + "..." if len(result["prompt_text"]) > 200 else result["prompt_text"]
            }
            
            for model in self.models:
                model_data = result["model_responses"][model]
                row = base_row.copy()
                row.update({
                    "model": model,
                    "success": model_data["success"],
                    "response_length": len(model_data["response"]) if model_data["response"] else 0,
                    "tokens_used": model_data["tokens_used"],
                    "error": model_data["error"]
                })
                rows.append(row)
        
        # Save to CSV
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False)
        print(f"📊 Detailed results exported to: {output_path}")

def main():
    """Main analyzer function"""
    import glob
    
    # Find the most recent results file
    results_files = glob.glob("evaluation_results_*.json")
    if not results_files:
        print("❌ No evaluation results found. Run model_evaluator.py first.")
        return
    
    latest_file = max(results_files, key=os.path.getctime)
    print(f"📊 Analyzing results from: {latest_file}")
    
    analyzer = ResultsAnalyzer(latest_file)
    
    # Generate and print report
    report = analyzer.generate_comparison_report()
    print(report)
    
    # Save report to file
    report_file = latest_file.replace('.json', '_report.txt')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n📝 Report saved to: {report_file}")
    
    # Export to CSV
    analyzer.export_to_csv()

if __name__ == "__main__":
    main() 