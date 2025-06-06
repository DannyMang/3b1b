import json
import os
from openai import OpenAI
import random

# Load existing datasets
with open("3b1b/dataset/data/manim_dataset.json", "r") as f:
    manim_dataset = json.load(f)

with open("3b1b/dataset/data/manim_doc_examples.json", "r") as f:
    doc_examples = json.load(f)

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Extract patterns, techniques, and code structures
def extract_code_snippets(dataset):
    snippets = []
    for item in dataset:
        if "output" in item and isinstance(item["output"], str):
            # Extract class definitions
            if "class " in item["output"]:
                snippets.append(item["output"].split("class ")[1].split(":")[0])
            # Extract common methods
            if "def construct" in item["output"]:
                construct_method = item["output"].split("def construct")[1]
                # Get the first few lines of the method
                method_lines = construct_method.split("\n")[:10]
                snippets.append("\n".join(method_lines))
    return snippets

# Generate synthetic examples
def generate_synthetic_example(prompt_template, snippets, existing_examples):
    # Create a prompt that combines patterns from existing examples
    sample_snippets = random.sample(snippets, min(3, len(snippets)))
    
    prompt = f"""
    Create a new Manim animation example that demonstrates a real-world use case.
    
    Here are some patterns from existing examples:
    ```
    {sample_snippets}
    ```
    
    Create a complete, working Manim animation class that:
    1. Has a descriptive name
    2. Implements the construct method
    3. Creates a visualization that would be useful in an educational context
    4. Uses common Manim objects and animations
    5. Is different from existing examples
    6. Is complete and not truncated
    
    The example should be in the format:
    ```python
    class ClassName(Scene):
        def construct(self):
            # Your code here
    ```
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in Manim animation programming."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    
    new_example = response.choices[0].message.content
    
    # Extract just the code part
    if "```python" in new_example:
        code = new_example.split("```python")[1].split("```")[0].strip()
    else:
        code = new_example
    
    # Extract class name
    class_name = code.split("class ")[1].split("(")[0].strip()
    
    return {
        "instruction": f"Create a Manim animation for {class_name}",
        "input": f"I need a Manim animation that demonstrates {class_name.lower()}",
        "output": code
    }

# Main process
snippets = extract_code_snippets(manim_dataset) + extract_code_snippets(doc_examples)

# Generate 50 new synthetic examples
synthetic_examples = []
for i in range(50):
    print(f"Generating example {i+1}/50...")
    example = generate_synthetic_example("Create a Manim animation", snippets, synthetic_examples)
    synthetic_examples.append(example)

# Save the synthetic dataset
with open("3b1b/dataset/data/synthetic_manim_dataset.json", "w") as f:
    json.dump(synthetic_examples, f, indent=2)

print(f"Generated {len(synthetic_examples)} synthetic examples") 