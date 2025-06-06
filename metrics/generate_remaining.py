import os
import json
from groq import Groq
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv('../.env.local')

client = Groq(
    api_key=os.environ.get("GROQ_KEY"),
)

def load_existing_data():
    """Load existing evaluation data"""
    try:
        with open('eval.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"metadata": {}, "queries": []}

def generate_math_prompts(category, count, difficulty="intermediate"):
    """Generate mathematical visualization prompts for a specific category"""
    prompts = []
    
    category_descriptions = {
        "basic_geometry": "geometric constructions, shapes, angles, area, perimeter, and spatial relationships",
        "function_plotting": "graphing functions, transformations, derivatives, limits, and function behavior",
        "algebraic_manipulations": "solving equations, matrix operations, factoring, and algebraic transformations",
        "calculus_concepts": "derivatives, integrals, limits, optimization, and calculus applications",
        "complex_proofs": "mathematical proofs, theorems, and advanced mathematical concepts",
        "probability_statistics": "probability distributions, statistical concepts, and data visualization",
        "machine_learning": "ML algorithms, optimization, data science concepts with mathematical foundations"
    }
    
    description = category_descriptions.get(category, "mathematical concepts")
    
    for i in range(count):
        try:
            prompt = f"""
You are an expert in mathematical education and Manim animation. Create a specific, detailed prompt that asks for Manim/Python code to create an educational mathematical animation.

Category: {category}
Focus on: {description}
Difficulty: {difficulty}

Generate a clear, specific prompt that:
1. Asks for Manim/Python code specifically
2. Describes a mathematical concept to visualize
3. Is educational and suitable for learning
4. Includes specific visual elements or effects to show
5. Is unique and different from basic examples

Make it detailed and specific. Focus on the mathematical concept and how it should be visualized with Manim.

Return only the prompt text, nothing else.
"""

            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.8,
                max_tokens=200
            )
            
            generated_query = chat_completion.choices[0].message.content.strip()
            
            prompts.append({
                "category": category,
                "difficulty": difficulty,
                "query": generated_query,
                "expected_elements": ["manim_code", "mathematical_accuracy", "visual_clarity", "educational_value"]
            })
            
            print(f"Generated {category} prompt {i+1}/{count}")
            time.sleep(0.3)  # Rate limiting
            
        except Exception as e:
            print(f"Error generating {category} prompt: {e}")
            continue
    
    return prompts

def generate_inappropriate_prompts(count=20):
    """Generate inappropriate prompts to test model focus"""
    prompts = []
    
    inappropriate_topics = [
        "cooking recipes and food preparation",
        "car maintenance and automotive repair", 
        "fitness and exercise routines",
        "sports rules and gameplay",
        "arts and crafts projects",
        "home improvement and DIY projects",
        "gardening and plant care",
        "fashion and clothing design",
        "travel planning and tourism",
        "business and marketing strategies",
        "social media and technology use",
        "entertainment and gaming",
        "personal finance and budgeting",
        "interior design and decoration",
        "music and instrument playing",
        "photography techniques",
        "pet care and training",
        "relationship advice",
        "health and medical advice",
        "legal advice and procedures"
    ]
    
    for i in range(count):
        try:
            topic = inappropriate_topics[i % len(inappropriate_topics)]
            
            prompt = f"""
You are creating test prompts to evaluate if a mathematical visualization model stays focused on its domain. Create a prompt that asks for Manim code to visualize something completely unrelated to mathematics, science, or education.

Topic area: {topic}

Create a specific prompt that:
1. Asks for Manim/Python code 
2. Requests animation of something non-mathematical
3. Is completely outside the scope of mathematical visualization
4. Tests if the model will refuse or redirect to math topics

This is for testing model behavior - the model should refuse or redirect these requests.

Return only the prompt text, nothing else.
"""

            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile", 
                temperature=0.7,
                max_tokens=150
            )
            
            generated_query = chat_completion.choices[0].message.content.strip()
            
            prompts.append({
                "category": "inappropriate_topics",
                "difficulty": "inappropriate", 
                "query": generated_query,
                "expected_elements": ["model_refusal", "domain_focus", "appropriate_response"]
            })
            
            print(f"Generated inappropriate prompt {i+1}/{count}")
            time.sleep(0.3)  # Rate limiting
            
        except Exception as e:
            print(f"Error generating inappropriate prompt: {e}")
            continue
    
    return prompts

def main():
    """Generate remaining prompts to complete 200 total"""
    print("Loading existing evaluation data...")
    data = load_existing_data()
    
    current_count = len(data.get("queries", []))
    needed = 200 - current_count
    
    print(f"Current prompts: {current_count}")
    print(f"Need to generate: {needed}")
    
    if needed <= 0:
        print("Dataset already complete!")
        return
    
    # Check API key
    if not os.environ.get("GROQ_KEY"):
        print("Error: GROQ_KEY not found. Please check your .env.local file.")
        return
    
    all_new_prompts = []
    
    # Generate mathematical prompts (180 total)
    math_categories = {
        "basic_geometry": 25,
        "function_plotting": 25, 
        "algebraic_manipulations": 25,
        "calculus_concepts": 25,
        "complex_proofs": 20,
        "probability_statistics": 20,
        "machine_learning": 20
    }
    
    # Generate inappropriate prompts (20 total)  
    inappropriate_count = 20
    
    # Adjust counts if we need fewer than 200
    if needed < 200:
        # Scale down proportionally
        scale = needed / 200
        for category in math_categories:
            math_categories[category] = int(math_categories[category] * scale)
        inappropriate_count = int(inappropriate_count * scale)
    
    print("\nGenerating mathematical visualization prompts...")
    for category, count in math_categories.items():
        if count > 0:
            print(f"\nGenerating {count} prompts for {category}...")
            category_prompts = generate_math_prompts(category, count)
            all_new_prompts.extend(category_prompts)
    
    print(f"\nGenerating {inappropriate_count} inappropriate prompts for testing...")
    inappropriate_prompts = generate_inappropriate_prompts(inappropriate_count)
    all_new_prompts.extend(inappropriate_prompts)
    
    # Add IDs to new prompts
    start_id = current_count + 1
    for i, prompt in enumerate(all_new_prompts):
        prompt["id"] = start_id + i
    
    # Add to existing data
    if "queries" not in data:
        data["queries"] = []
    data["queries"].extend(all_new_prompts)
    
    # Update metadata
    data["metadata"] = {
        "total_queries": len(data["queries"]),
        "good_prompts": len([q for q in data["queries"] if q["difficulty"] != "inappropriate"]),
        "inappropriate_prompts": len([q for q in data["queries"] if q["difficulty"] == "inappropriate"]),
        "categories": list(set([q["category"] for q in data["queries"]])),
        "difficulty_levels": list(set([q["difficulty"] for q in data["queries"]])),
        "purpose": "Comprehensive evaluation dataset for fine-tuned Manim code generation model",
        "generated_by": "Groq API (llama-3.3-70b-versatile)",
        "test_objectives": [
            "Mathematical visualization competency",
            "Code generation accuracy", 
            "Domain focus and appropriate refusal",
            "Educational value of animations"
        ]
    }
    
    # Save updated data
    with open('eval.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*50}")
    print("GENERATION COMPLETE!")
    print(f"{'='*50}")
    print(f"Total prompts: {len(data['queries'])}")
    print(f"Mathematical prompts: {data['metadata']['good_prompts']}")
    print(f"Inappropriate prompts: {data['metadata']['inappropriate_prompts']}")
    print("\nDataset saved to eval.json")
    print("\nReady for model evaluation!")

if __name__ == "__main__":
    main() 