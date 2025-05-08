import json
import os
from typing import Dict, Any
import re

class DatasetEditor:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.dataset = []
        self.current_index = 0
        self.load_dataset()
        
    def load_dataset(self):
        """Load the dataset from JSON file"""
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            self.dataset = json.load(f)
            
    def save_dataset(self):
        """Save the dataset back to JSON file"""
        with open(self.dataset_path, 'w', encoding='utf-8') as f:
            json.dump(self.dataset, f, indent=2)
            
    def get_current_entry(self) -> Dict[str, Any]:
        """Get the current entry being viewed"""
        return self.dataset[self.current_index]
    
    def update_current_entry(self, instruction: str = None, input_text: str = None, output: str = None):
        """Update the current entry with new values"""
        if instruction is not None:
            self.dataset[self.current_index]['instruction'] = instruction
        if input_text is not None:
            self.dataset[self.current_index]['input'] = input_text
        if output is not None:
            self.dataset[self.current_index]['output'] = output
            
    def add_manim_imports(self):
        """Add standard Manim imports to the current entry's output"""
        output = self.dataset[self.current_index]['output']
        if 'from manim import' not in output:
            imports = "from manim import *\n\n"
            self.dataset[self.current_index]['output'] = imports + output
            
    def fix_construct_method(self):
        """Ensure the current entry has a construct method"""
        output = self.dataset[self.current_index]['output']
        if 'def construct' not in output:
            # Find the class definition
            class_match = re.search(r'class\s+\w+\s*\(\s*Scene\s*\)', output)
            if class_match:
                class_end = class_match.end()
                new_output = output[:class_end] + ":\n    def construct(self):\n        pass\n" + output[class_end:]
                self.dataset[self.current_index]['output'] = new_output
                
    def display_current_entry(self):
        """Display the current entry in a readable format"""
        entry = self.get_current_entry()
        print("\n" + "="*80)
        print(f"Entry {self.current_index + 1} of {len(self.dataset)}")
        print("="*80)
        print("\nInstruction:")
        print("-"*40)
        print(entry['instruction'])
        print("\nInput:")
        print("-"*40)
        print(entry['input'])
        print("\nOutput:")
        print("-"*40)
        print(entry['output'])
        print("="*80)
        
    def interactive_edit(self):
        """Start interactive editing session"""
        while True:
            self.display_current_entry()
            print("\nCommands:")
            print("n - Next entry")
            print("p - Previous entry")
            print("i - Edit instruction")
            print("t - Edit input text")
            print("o - Edit output code")
            print("m - Add Manim imports")
            print("c - Fix construct method")
            print("s - Save changes")
            print("q - Quit")
            
            cmd = input("\nEnter command: ").lower()
            
            if cmd == 'q':
                if input("Save changes before quitting? (y/n): ").lower() == 'y':
                    self.save_dataset()
                break
            elif cmd == 'n':
                if self.current_index < len(self.dataset) - 1:
                    self.current_index += 1
            elif cmd == 'p':
                if self.current_index > 0:
                    self.current_index -= 1
            elif cmd == 'i':
                new_instruction = input("Enter new instruction: ")
                self.update_current_entry(instruction=new_instruction)
            elif cmd == 't':
                new_input = input("Enter new input text: ")
                self.update_current_entry(input_text=new_input)
            elif cmd == 'o':
                print("Enter new output code (type 'END' on a new line to finish):")
                lines = []
                while True:
                    line = input()
                    if line == 'END':
                        break
                    lines.append(line)
                new_output = '\n'.join(lines)
                self.update_current_entry(output=new_output)
            elif cmd == 'm':
                self.add_manim_imports()
            elif cmd == 'c':
                self.fix_construct_method()
            elif cmd == 's':
                self.save_dataset()
                print("Changes saved!")

def main():
    editor = DatasetEditor('./dataset/data/manim_dataset.json')
    editor.interactive_edit()

if __name__ == "__main__":
    main() 