import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from manim_generator import ManimGenerator
import os
from config import Config

class NL2Manim:
    def __init__(self):
        self.model = AutoModelForCausalLM.from_pretrained(Config.MODEL_NAME)
        self.tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
        self.manim_generator = ManimGenerator()
        
    def process_instruction(self, instruction: str) -> str:
        """
        Process natural language instruction and generate Manim code
        """
        # Tokenize the instruction
        inputs = self.tokenizer(instruction, return_tensors="pt", max_length=Config.MAX_LENGTH, truncation=True)
        
        # Generate structured output using the model
        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_length=Config.MAX_LENGTH,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9
            )
        
        # Decode the generated output
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Convert to Manim code
        manim_code = self.manim_generator.generate_code(generated_text)
        
        return manim_code
    
    def save_and_render(self, code: str, filename: str = "generated_scene.py"):
        """
        Save the generated code and render the animation
        """
        with open(filename, "w") as f:
            f.write(code)
        
        # Render the animation
        os.system(f"manim -pql {filename} GeneratedScene")

def main():
    # Initialize the NL2Manim system
    nl2manim = NL2Manim()
    
    # Example instruction
    instruction = "Create a circle that transforms into a square"
    
    # Process the instruction
    manim_code = nl2manim.process_instruction(instruction)
    
    # Save and render the animation
    nl2manim.save_and_render(manim_code)

if __name__ == "__main__":
    main() 