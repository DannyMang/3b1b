import subprocess
import tempfile
import os
import re
import json

def validate_manim_code(code):
    """
    Validates if the Manim code is syntactically correct and follows best practices.
    Returns (is_valid, error_message)
    """
    # Check for basic Python syntax
    try:
        compile(code, '<string>', 'exec')
    except SyntaxError as e:
        return False, f"Syntax error: {str(e)}"
    
    # Check for required Manim imports
    if "from manim import" not in code and "import manim" not in code:
        return False, "Missing Manim imports"
    
    # Check for Scene class inheritance
    if not re.search(r"class\s+\w+\s*\(\s*(?:Scene|MovingCameraScene|ThreeDScene)\s*\)", code):
        return False, "Animation class must inherit from Scene, MovingCameraScene, or ThreeDScene"
    
    # Check for construct method
    if "def construct(self):" not in code:
        return False, "Missing construct method"
    
    return True, ""

def test_run_manim_code(code, class_name):
    """
    Attempts to run the Manim code and generate a video.
    Returns (success, output_path or error_message)
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp_file:
        temp_file_path = temp_file.name
        temp_file.write(code.encode('utf-8'))
    
    try:
        # Run manim on the temporary file
        output_dir = os.path.join(os.getcwd(), "media", "videos")
        os.makedirs(output_dir, exist_ok=True)
        
        cmd = ["manim", "-pql", temp_file_path, class_name]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            return False, f"Manim execution failed: {result.stderr}"
        
        # Extract the output video path from stdout
        video_path_match = re.search(r"File ready at '(.+?)'", result.stdout)
        if video_path_match:
            return True, video_path_match.group(1)
        else:
            return True, "Video generated but path not found in output"
    
    except subprocess.TimeoutExpired:
        return False, "Execution timed out (60s limit)"
    except Exception as e:
        return False, f"Error running Manim: {str(e)}"
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

# Example usage for validating synthetic examples
def validate_synthetic_dataset():
    with open("3b1b/dataset/data/synthetic_manim_dataset.json", "r") as f:
        synthetic_examples = json.load(f)
    
    valid_examples = []
    invalid_examples = []
    
    for i, example in enumerate(synthetic_examples):
        code = example["output"]
        class_name = code.split("class ")[1].split("(")[0].strip()
        
        print(f"Validating example {i+1}/{len(synthetic_examples)}: {class_name}")
        
        # First check syntax and structure
        is_valid, error_message = validate_manim_code(code)
        if not is_valid:
            print(f"  Failed validation: {error_message}")
            invalid_examples.append((example, error_message))
            continue
        
        # Then try to run it
        success, result = test_run_manim_code(code, class_name)
        if success:
            print(f"  Success! Video generated at: {result}")
            example["video_path"] = result
            valid_examples.append(example)
        else:
            print(f"  Failed execution: {result}")
            invalid_examples.append((example, result))
    
    # Save validated examples
    with open("3b1b/dataset/data/validated_synthetic_dataset.json", "w") as f:
        json.dump(valid_examples, f, indent=2)
    
    print(f"Validation complete: {len(valid_examples)} valid, {len(invalid_examples)} invalid")
    return valid_examples, invalid_examples

if __name__ == "__main__":
    validate_synthetic_dataset() 