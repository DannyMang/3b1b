import json
import re
from bs4 import BeautifulSoup
import os

class ManimDocParser:
    def __init__(self):
        self.examples = []
        
    def parse_html(self, html_content):
        """Parse HTML content and extract examples."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all code blocks
        code_blocks = soup.find_all(['div', 'pre'], class_=['highlight-python', 'highlight-python3', 'python'])
        
        for block in code_blocks:
            # Get the code
            code = block.find('pre').text.strip() if block.name == 'div' else block.text.strip()
            
            # Get the section title or context
            section = block.find_previous(['h1', 'h2', 'h3'])
            section_title = section.text.strip() if section else "Unknown Section"
            
            # Get the description if available
            description = ""
            prev_elem = block.find_previous(['p', 'div'])
            if prev_elem and prev_elem.name == 'p':
                description = prev_elem.text.strip()
            
            # Create instruction and input
            instruction = f"Create a 3B1B-style Manim animation for {section_title}"
            input_text = f"I need a 3B1B-style animation that {description.lower() if description else section_title.lower()}"
            
            # Format as Alpaca example
            example = {
                "instruction": instruction,
                "input": input_text,
                "output": code
            }
            
            self.examples.append(example)
    
    def save_examples(self, filename='manim_doc_examples.json'):
        """Save the parsed examples to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.examples, f, indent=2)
        print(f"Saved {len(self.examples)} examples to {filename}")

def main():
    parser = ManimDocParser()
    
    # Read the HTML files
    html_files = ['examples.txt', 'mainpage.txt', 'tutorial.txt']
    for file in html_files:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                html_content = f.read()
                parser.parse_html(html_content)
    
    # Save the examples
    parser.save_examples()

if __name__ == "__main__":
    main() 