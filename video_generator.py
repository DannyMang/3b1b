import os
import subprocess
from datetime import datetime

def clean_manim_code(code: str) -> str:
    """
    Clean the AI-generated Manim code by removing think tags and ensuring it's valid Python.
    """
    # Remove think tags and their content
    if "<think>" in code:
        code = code.split("</think>")[-1]
    
    # Ensure the code starts with imports
    if not code.strip().startswith("from manim import"):
        code = "from manim import *\n\n" + code
    
    return code

def generate_video_from_code(code: str, output_dir: str = "videos") -> str:
    """
    Generate a video from Manim code.
    
    Args:
        code (str): The Manim code to render
        output_dir (str): Directory to save the video
        
    Returns:
        str: Path to the generated video
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a unique filename based on timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_file = f"temp_animation_{timestamp}.py"
    output_file = os.path.join(output_dir, f"animation_{timestamp}.mp4")
    
    try:
        # Clean and write the code to a temporary file
        cleaned_code = clean_manim_code(code)
        with open(temp_file, "w") as f:
            f.write(cleaned_code)
        
        # Run manim command to render the video
        command = [
            "manim",
            "-qh",  # High quality
            "-o", output_file,  # Output file
            temp_file,  # Input file
            "TransformerArchitecture"  # Scene class name
        ]
        
        subprocess.run(command, check=True)
        
        print(f"Video generated successfully: {output_file}")
        return output_file
        
    except subprocess.CalledProcessError as e:
        print(f"Error generating video: {e}")
        return None
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    # Example usage
    sample_code = """
from manim import *

class TransformerArchitecture(Scene):
    def construct(self):
        title = Text("Transformer Architecture")
        self.play(Write(title))
        self.wait(2)
"""
    
    video_path = generate_video_from_code(sample_code)
    if video_path:
        print(f"Video saved at: {video_path}") 