import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any
import glob

class DatasetScraper:
    def __init__(self):
        self.dataset = []
        self.manim_path = "../manim"
        self.videos_path = "../videos"
        
    def extract_from_manim_examples(self):
        """Extract examples from Manim's example_scenes directory"""
        examples_path = os.path.join(self.manim_path, "example_scenes")
        
        for py_file in glob.glob(os.path.join(examples_path, "**/*.py"), recursive=True):
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract classes that inherit from Scene
            scene_pattern = re.compile(r'class\s+(\w+)\s*\(\s*Scene\s*\)[^{]*:[\s\S]*?(?=class|\Z)')
            for match in scene_pattern.finditer(content):
                scene_code = match.group(0)
                scene_name = re.search(r'class\s+(\w+)', scene_code).group(1)
                
                # Extract docstring if it exists
                docstring = ""
                doc_match = re.search(r'"""([\s\S]*?)"""', scene_code)
                if doc_match:
                    docstring = doc_match.group(1).strip()
                
                # Create instruction and input
                instruction = f"Create a Manim animation for {scene_name.replace('_', ' ')}"
                input_text = f"I need an animation that {docstring if docstring else scene_name.replace('_', ' ').lower()}"
                
                self.dataset.append({
                    "instruction": instruction,
                    "input": input_text,
                    "output": scene_code
                })

    def extract_from_3b1b_videos(self):
        """Extract examples from 3B1B's videos repository (last 5 years)"""
        # Get the last 5 years
        current_year = 2024
        years = [str(year) for year in range(current_year-4, current_year+1)]
        
        for year in years:
            year_dir = os.path.join(self.videos_path, f"_{year}")
            if not os.path.exists(year_dir):
                continue
                
            for py_file in glob.glob(os.path.join(year_dir, "**/*.py"), recursive=True):
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract classes that inherit from Scene
                scene_pattern = re.compile(r'class\s+(\w+)\s*\(\s*Scene\s*\)[^{]*:[\s\S]*?(?=class|\Z)')
                for match in scene_pattern.finditer(content):
                    scene_code = match.group(0)
                    scene_name = re.search(r'class\s+(\w+)', scene_code).group(1)
                    
                    # Extract docstring if it exists
                    docstring = ""
                    doc_match = re.search(r'"""([\s\S]*?)"""', scene_code)
                    if doc_match:
                        docstring = doc_match.group(1).strip()
                    
                    # Create instruction and input
                    instruction = f"Create a 3B1B-style Manim animation for {scene_name.replace('_', ' ')}"
                    input_text = f"I need a 3B1B-style animation that {docstring if docstring else scene_name.replace('_', ' ').lower()}"
                    
                    self.dataset.append({
                        "instruction": instruction,
                        "input": input_text,
                        "output": scene_code
                    })

    def save_dataset(self, output_path: str = "manim_dataset.json"):
        """Save the dataset to a JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.dataset, f, indent=2)
        print(f"Dataset created with {len(self.dataset)} examples")

def main():
    scraper = DatasetScraper()
    
    print("Extracting examples from Manim library...")
    scraper.extract_from_manim_examples()
    
    print("Extracting examples from 3B1B videos...")
    scraper.extract_from_3b1b_videos()
    
    print("Saving dataset...")
    scraper.save_dataset()

if __name__ == "__main__":
    main() 