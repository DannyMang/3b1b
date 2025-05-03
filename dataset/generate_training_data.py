import json
from typing import List, Dict, Optional
import os

def create_training_example(instruction: str, output_code: str, input_text: Optional[str] = None) -> Dict:
    """
    Create a single training example in Alpaca format
    Args:
        instruction: Natural language description of the animation
        output_code: The Manim code that creates the animation
        input_text: Optional additional context or parameters
    """
    example = {
        "instruction": instruction,
        "output": output_code
    }
    if input_text:
        example["input"] = input_text
    return example

def save_dataset(examples: List[Dict], filename: str):
    """
    Save examples to a JSON file
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(examples, f, indent=2)

def main():
    """
    
    to -do 
    - need to find way to automate loading data from community projects or whatnot. 
    - need to figure out how to correctly clean data
    - for training/test we can just do 70:30 split w/ k-fold cross validation 
    
     
    """

if __name__ == "__main__":
    main()