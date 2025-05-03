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
    # Example training data
    examples = [
        # Example without input
        create_training_example(
            "Create a circle that transforms into a square",
            """from manim import *

class GeneratedScene(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        self.play(Create(circle))
        self.play(Transform(circle, square))"""
        ),
        # Example with input
        create_training_example(
            "Show a bouncing ball with gravity",
            """from manim import *

class BouncingBall(Scene):
    def construct(self):
        ball = Circle(radius=0.5, color=RED)
        self.play(Create(ball))
        self.play(ball.animate.shift(DOWN * 2), rate_func=rate_functions.ease_in_out)""",
            input_text="ball_color: RED, gravity: 9.8"
        )
    ]
    
    # Save training and validation sets
    train_examples = examples[:1]  # First example for training
    val_examples = examples[1:]    # Second example for validation
    
    save_dataset(train_examples, "dataset/train.json")
    save_dataset(val_examples, "dataset/validation.json")

if __name__ == "__main__":
    main() 