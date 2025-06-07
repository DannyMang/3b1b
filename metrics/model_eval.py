import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any
from openai import OpenAI
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv('.env.local')

class ModelEvaluator:
    """Evaluates multiple models against a dataset of prompts and logs responses"""
    
    def __init__(self):
        # Initialize OpenRouter client for external models
        self.openrouter_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv('OPENROUTER_API_KEY')
        )
        
        # Initialize HuggingFace client for fine-tuned model
        self.hf_client = OpenAI(
            base_url=os.getenv('HUGGINGFACE_BASE_URL'),
            api_key=os.getenv('HUGGINGFACE_API_KEY')
        )
        
        # Define models to test
        self.models = {
            "fine_tuned_manim": {
                "client": "huggingface",
                "model_name": "tgi",
                "description": "Fine-tuned Manim code generation model"
            },
            "gpt4o": {
                "client": "openrouter", 
                "model_name": "openai/gpt-4o",
                "description": "OpenAI GPT-4o"
            },
            "claude_sonnet": {
                "client": "openrouter",
                "model_name": "anthropic/claude-3.5-sonnet",
                "description": "Anthropic Claude 3.5 Sonnet"
            },
            "gemini_pro": {
                "client": "openrouter",
                "model_name": "google/gemini-pro-1.5",
                "description": "Google Gemini Pro 1.5"
            },
            "llama_405b": {
                "client": "openrouter",
                "model_name": "meta-llama/llama-3.1-405b-instruct",
                "description": "Meta Llama 3.1 405B Instruct"
            }
        }
        
        # Initialize results storage
        self.results = {
            "metadata": {
                "evaluation_start": None,
                "evaluation_end": None,
                "total_prompts": 0,
                "models_tested": list(self.models.keys()),
                "dataset_file": None
            },
            "results": []
        }
    
    def load_evaluation_dataset(self, dataset_path: str) -> List[Dict]:
        """Load the evaluation dataset"""
        try:
            with open(dataset_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.results["metadata"]["dataset_file"] = dataset_path
            self.results["metadata"]["total_prompts"] = len(data["queries"])
            
            print(f"✅ Loaded {len(data['queries'])} evaluation prompts")
            return data["queries"]
        
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return []
    
    def call_model(self, model_key: str, prompt: str, max_tokens: int = 2048) -> Dict[str, Any]:
        """Call a specific model with the given prompt"""
        model_config = self.models[model_key]
        
        try:
            if model_config["client"] == "huggingface":
                # Call fine-tuned model
                response = self.hf_client.chat.completions.create(
                    model=model_config["model_name"],
                    messages=[
                        {
                            "role": "user",
                            "content": f"{prompt}\nPlease provide complete, runnable Manim code."
                        }
                    ],
                    max_tokens=max_tokens,
                    stream=False
                )
                
                return {
                    "success": True,
                    "response": response.choices[0].message.content,
                    "model": model_key,
                    "tokens_used": getattr(response.usage, 'total_tokens', None) if hasattr(response, 'usage') else None,
                    "error": None
                }
                
            elif model_config["client"] == "openrouter":
                # Call OpenRouter model
                response = self.openrouter_client.chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": "https://github.com/your-repo",
                        "X-Title": "Manim Model Evaluation"
                    },
                    model=model_config["model_name"],
                    messages=[
                        {
                            "role": "user", 
                            "content": f"{prompt}\nPlease provide complete, runnable Manim code for creating this mathematical visualization."
                        }
                    ],
                    max_tokens=max_tokens
                )
                
                return {
                    "success": True,
                    "response": response.choices[0].message.content,
                    "model": model_key,
                    "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None,
                    "error": None
                }
        
        except Exception as e:
            return {
                "success": False,
                "response": None,
                "model": model_key,
                "tokens_used": None,
                "error": str(e)
            }
    
    def evaluate_single_prompt(self, prompt_data: Dict) -> Dict[str, Any]:
        """Evaluate a single prompt across all models"""
        prompt_id = prompt_data["id"]
        prompt_text = prompt_data["query"]
        category = prompt_data["category"]
        difficulty = prompt_data["difficulty"]
        
        print(f"\n🔄 Evaluating Prompt {prompt_id}: {category} ({difficulty})")
        print(f"   Prompt: {prompt_text[:80]}...")
        
        prompt_results = {
            "prompt_id": prompt_id,
            "prompt_text": prompt_text,
            "category": category,
            "difficulty": difficulty,
            "expected_elements": prompt_data["expected_elements"],
            "timestamp": datetime.now().isoformat(),
            "model_responses": {}
        }
        
        # Test each model
        for model_key in self.models.keys():
            print(f"   📡 Testing {model_key}...")
            
            result = self.call_model(model_key, prompt_text)
            prompt_results["model_responses"][model_key] = result
            
            if result["success"]:
                response_preview = result["response"][:100] if result["response"] else "No response"
                print(f"      ✅ Success: {response_preview}...")
            else:
                print(f"      ❌ Failed: {result['error']}")
            
            # Rate limiting for OpenRouter
            time.sleep(1)
        
        return prompt_results
    
    def run_evaluation(self, dataset_path: str, output_path: str = None, limit: int = None):
        """Run complete evaluation across all models and prompts"""
        print("🚀 Starting Model Evaluation")
        print("="*60)
        
        # Load dataset
        prompts = self.load_evaluation_dataset(dataset_path)
        if not prompts:
            print("❌ No prompts to evaluate")
            return
        
        # Limit prompts for testing if specified
        if limit:
            prompts = prompts[:limit]
            print(f"🔬 Testing with limited dataset: {limit} prompts")
        
        # Set metadata
        self.results["metadata"]["evaluation_start"] = datetime.now().isoformat()
        self.results["metadata"]["total_prompts"] = len(prompts)
        
        # Evaluate each prompt
        for i, prompt_data in enumerate(prompts):
            try:
                prompt_result = self.evaluate_single_prompt(prompt_data)
                self.results["results"].append(prompt_result)
                
                # Save intermediate results every 10 prompts
                if (i + 1) % 10 == 0:
                    self.save_results(output_path, intermediate=True)
                    print(f"📊 Progress: {i + 1}/{len(prompts)} prompts completed")
                
            except Exception as e:
                print(f"❌ Error evaluating prompt {prompt_data['id']}: {e}")
                print(traceback.format_exc())
        
        # Finalize evaluation
        self.results["metadata"]["evaluation_end"] = datetime.now().isoformat()
        
        # Save final results
        final_output = self.save_results(output_path)
        
        # Print summary
        self.print_evaluation_summary()
        
        return final_output
    
    def save_results(self, output_path: str = None, intermediate: bool = False) -> str:
        """Save evaluation results to JSON file"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            suffix = "_intermediate" if intermediate else ""
            output_path = f"evaluation_results_{timestamp}{suffix}.json"
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            if not intermediate:
                print(f"💾 Final results saved to: {output_path}")
            
            return output_path
        
        except Exception as e:
            print(f"❌ Error saving results: {e}")
            return None
    
    def print_evaluation_summary(self):
        """Print summary of evaluation results"""
        print("\n" + "="*60)
        print("📊 EVALUATION SUMMARY")
        print("="*60)
        
        total_prompts = len(self.results["results"])
        print(f"Total prompts evaluated: {total_prompts}")
        
        # Success rates by model
        print("\n🏆 Model Success Rates:")
        for model_key in self.models.keys():
            successes = sum(1 for r in self.results["results"] 
                          if r["model_responses"][model_key]["success"])
            success_rate = (successes / total_prompts) * 100 if total_prompts > 0 else 0
            print(f"   {model_key}: {successes}/{total_prompts} ({success_rate:.1f}%)")
        
        # Category breakdown
        print("\n📂 Performance by Category:")
        categories = {}
        for result in self.results["results"]:
            cat = result["category"]
            if cat not in categories:
                categories[cat] = {"total": 0, "model_successes": {}}
            
            categories[cat]["total"] += 1
            for model_key in self.models.keys():
                if model_key not in categories[cat]["model_successes"]:
                    categories[cat]["model_successes"][model_key] = 0
                
                if result["model_responses"][model_key]["success"]:
                    categories[cat]["model_successes"][model_key] += 1
        
        for cat, data in categories.items():
            print(f"\n   {cat} ({data['total']} prompts):")
            for model_key in self.models.keys():
                success_rate = (data["model_successes"][model_key] / data["total"]) * 100
                print(f"      {model_key}: {success_rate:.1f}%")

def main():
    """Main evaluation function"""
    evaluator = ModelEvaluator()
    
    # Check required environment variables
    required_vars = ['OPENROUTER_API_KEY', 'HUGGINGFACE_BASE_URL', 'HUGGINGFACE_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env.local file")
        return
    
    # Run evaluation
    dataset_path = "metrics/evaluation_dataset_complete.json"
    
    print("🎯 Model Evaluation Options:")
    print("1. Run full evaluation (200 prompts)")
    print("2. Run test evaluation (10 prompts)")
    print("3. Run category-specific evaluation")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        evaluator.run_evaluation(dataset_path)
    elif choice == "2":
        evaluator.run_evaluation(dataset_path, limit=10)
    elif choice == "3":
        print("Category-specific evaluation not yet implemented")
    else:
        print("Invalid choice. Running test evaluation...")
        evaluator.run_evaluation(dataset_path, limit=10)

if __name__ == "__main__":
    main() 