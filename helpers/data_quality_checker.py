import json
import ast
import re
from typing import List, Dict, Any
from collections import Counter

class DataQualityChecker:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.dataset = []
        self.issues = []
        
    def load_dataset(self):
        """Load the dataset from JSON file"""
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            self.dataset = json.load(f)
            
    def check_code_validity(self):
        """Check if all code examples are valid Python"""
        for idx, example in enumerate(self.dataset):
            try:
                ast.parse(example['output'])
            except SyntaxError as e:
                self.issues.append(f"Invalid Python code in example {idx}: {str(e)}")
                
    def check_scene_inheritance(self):
        """Verify that all code examples inherit from Scene"""
        for idx, example in enumerate(self.dataset):
            if 'class' not in example['output'] or 'Scene' not in example['output']:
                self.issues.append(f"Example {idx} does not contain a Scene class")
                
    def check_duplicates(self):
        """Check for duplicate examples"""
        code_hashes = Counter()
        for idx, example in enumerate(self.dataset):
            code_hash = hash(example['output'])
            if code_hash in code_hashes:
                self.issues.append(f"Duplicate code found: example {idx} matches example {code_hashes[code_hash]}")
            code_hashes[code_hash] = idx
            
    def check_instruction_quality(self):
        """Check quality of instructions and inputs"""
        for idx, example in enumerate(self.dataset):
            if len(example['instruction']) < 10:
                self.issues.append(f"Example {idx} has too short instruction")
            if len(example['input']) < 10:
                self.issues.append(f"Example {idx} has too short input")
                
    def check_code_completeness(self):
        """Check if code examples are complete"""
        for idx, example in enumerate(self.dataset):
            code = example['output']
            if not re.search(r'def\s+construct\s*\(', code):
                self.issues.append(f"Example {idx} missing construct method")
            if not re.search(r'from\s+manim\s+import', code):
                self.issues.append(f"Example {idx} missing Manim imports")
                
    def analyze_dataset_stats(self):
        """Analyze dataset statistics"""
        stats = {
            'total_examples': len(self.dataset),
            'avg_instruction_length': sum(len(ex['instruction']) for ex in self.dataset) / len(self.dataset),
            'avg_input_length': sum(len(ex['input']) for ex in self.dataset) / len(self.dataset),
            'avg_code_length': sum(len(ex['output']) for ex in self.dataset) / len(self.dataset),
        }
        return stats
        
    def run_all_checks(self):
        """Run all quality checks"""
        self.load_dataset()
        self.check_code_validity()
        self.check_scene_inheritance()
        self.check_duplicates()
        self.check_instruction_quality()
        self.check_code_completeness()
        
        stats = self.analyze_dataset_stats()
        
        print("\nDataset Statistics:")
        for key, value in stats.items():
            print(f"{key}: {value}")
            
        print("\nIssues Found:")
        for issue in self.issues:
            print(f"- {issue}")
            
        return len(self.issues) == 0

def main():
    checker = DataQualityChecker('./dataset/data/manim_dataset.json')
    is_valid = checker.run_all_checks()
    print(f"\nDataset is {'valid' if is_valid else 'invalid'}")

if __name__ == "__main__":
    main() 