import json
from groq import Groq  
from dotenv import load_dotenv
import os
import time

load_dotenv('../.env.local')
client = Groq(api_key=os.environ.get('GROQ_KEY'))

# Load current data
with open('eval.json', 'r') as f:
    data = json.load(f)

print(f'Current total: {len(data["queries"])}')
needed = 200 - len(data['queries'])
print(f'Need {needed} more prompts')

# Generate remaining prompts
new_prompts = []
for i in range(needed):
    try:
        if i < needed - 1:  # Mathematical prompts
            prompt = 'Create a detailed prompt asking for Manim/Python code to create an educational mathematical animation. Focus on advanced topics like topology, number theory, abstract algebra, or mathematical physics. Make it specific and educational.'
            category = 'advanced_mathematics'
            difficulty = 'advanced'
            expected = ['manim_code', 'mathematical_accuracy', 'visual_clarity']
        else:  # One more inappropriate prompt
            prompt = 'Create a prompt asking for Manim code to animate something completely unrelated to mathematics - like pet grooming, home organization, or hobby crafts. This tests model focus.'
            category = 'inappropriate_topics'  
            difficulty = 'inappropriate'
            expected = ['model_refusal', 'domain_focus']
            
        response = client.chat.completions.create(
            messages=[{'role': 'user', 'content': prompt}],
            model='llama-3.3-70b-versatile',
            temperature=0.8,
            max_tokens=200
        )
        
        query = response.choices[0].message.content.strip()
        new_prompts.append({
            'id': len(data['queries']) + len(new_prompts) + 1,
            'category': category,
            'difficulty': difficulty, 
            'query': query,
            'expected_elements': expected
        })
        
        print(f'Generated prompt {len(new_prompts)}/{needed}')
        time.sleep(0.3)
        
    except Exception as e:
        print(f'Error: {e}')

# Add new prompts
data['queries'].extend(new_prompts)

# Update metadata
data['metadata']['total_queries'] = len(data['queries'])  
data['metadata']['good_prompts'] = len([q for q in data['queries'] if q['difficulty'] != 'inappropriate'])
data['metadata']['inappropriate_prompts'] = len([q for q in data['queries'] if q['difficulty'] == 'inappropriate'])

# Save
with open('eval.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f'Final total: {len(data["queries"])} prompts')
print('Dataset complete!') 