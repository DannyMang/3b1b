import json
import random

# Create a list of non-Manim tasks
non_manim_tasks = [
    "Solve this math problem: Find the integral of x^2 * sin(x)",
    "Write a Python script to analyze stock market data",
    "Help me with my homework on linear algebra",
    "Create a website using HTML and CSS",
    "Explain quantum computing to me",
    "Write a cover letter for a job application",
    "Debug this JavaScript code",
    "Give me tips for learning machine learning",
    "How do I install TensorFlow?",
    "What's the best way to learn calculus?",
    "Can you write a poem about mathematics?",
    "Explain how blockchain works",
    "Help me with my taxes",
    "Write a function to sort an array in Python",
    "What's the difference between SQL and NoSQL?",
    "How do I create a neural network?",
    "Write a regex to match email addresses",
    "Explain P vs NP problem",
    "How do I use pandas for data analysis?",
    "Write a script to automate file renaming"
]

# Create polite rejection responses
rejection_responses = [
    "I'm specialized in creating Manim animations for mathematical visualizations. I can help you create a Manim animation related to {topic}, but I can't {task_type}. Would you like me to create a visualization instead?",
    "As a Manim specialist, I focus on creating mathematical animations. While I can't {task_type}, I'd be happy to help you create a Manim animation that demonstrates {topic} concepts.",
    "I'm designed specifically to help with Manim animations for math visualizations. I can't {task_type}, but I can create a Manim animation that illustrates {topic} if you're interested.",
    "My expertise is in creating Manim animations for educational purposes. I can't {task_type}, but I can help you visualize {topic} using Manim if that would be helpful.",
    "I'm a Manim animation specialist, so I can't {task_type}. However, I'd be happy to help you create a mathematical visualization related to {topic} using Manim."
]

# Map tasks to topics and task types
task_mappings = {
    "math problem": {"topic": "calculus", "task_type": "solve math problems directly"},
    "Python script": {"topic": "algorithms", "task_type": "write general Python scripts"},
    "homework": {"topic": "mathematical concepts", "task_type": "do homework assignments"},
    "website": {"topic": "mathematical concepts", "task_type": "create websites"},
    "quantum computing": {"topic": "quantum mechanics", "task_type": "provide general explanations"},
    "cover letter": {"topic": "professional development", "task_type": "write cover letters"},
    "JavaScript": {"topic": "algorithms", "task_type": "debug JavaScript code"},
    "machine learning": {"topic": "data science", "task_type": "provide general learning advice"},
    "TensorFlow": {"topic": "machine learning", "task_type": "provide installation instructions"},
    "calculus": {"topic": "calculus", "task_type": "provide general learning advice"},
    "poem": {"topic": "mathematics", "task_type": "write creative content"},
    "blockchain": {"topic": "cryptography", "task_type": "explain technical concepts"},
    "taxes": {"topic": "financial calculations", "task_type": "help with taxes"},
    "sort an array": {"topic": "algorithms", "task_type": "write general programming functions"},
    "SQL": {"topic": "data structures", "task_type": "explain database concepts"},
    "neural network": {"topic": "machine learning", "task_type": "create neural networks"},
    "regex": {"topic": "pattern matching", "task_type": "write regular expressions"},
    "P vs NP": {"topic": "computational complexity", "task_type": "explain theoretical computer science"},
    "pandas": {"topic": "data analysis", "task_type": "provide pandas tutorials"},
    "automate": {"topic": "automation", "task_type": "write automation scripts"}
}

# Create rejection examples
rejection_examples = []

for task in non_manim_tasks:
    # Find the matching topic and task type
    topic = "mathematics"
    task_type = "provide general assistance"
    
    for key, mapping in task_mappings.items():
        if key in task.lower():
            topic = mapping["topic"]
            task_type = mapping["task_type"]
            break
    
    # Choose a random rejection response
    response = random.choice(rejection_responses).format(topic=topic, task_type=task_type)
    
    # Create the example
    example = {
        "instruction": "Handle a non-Manim request appropriately",
        "input": task,
        "output": response
    }
    
    rejection_examples.append(example)

# Save the rejection examples
with open("3b1b/dataset/data/rejection_examples.json", "w") as f:
    json.dump(rejection_examples, f, indent=2)

print(f"Created {len(rejection_examples)} rejection examples") 