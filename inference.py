from openai import OpenAI
import os
from dotenv import load_dotenv
from video_generator import generate_video_from_code

# Load environment variables from .env file
load_dotenv('.env.local')

# Initialize the OpenAI client with the Hugging Face endpoint
client = OpenAI(
    base_url=os.getenv('HUGGINGFACE_BASE_URL'),
    api_key=os.getenv('HUGGINGFACE_API_KEY')
)

def generate_animation_code(prompt):
    print(f"Sending prompt: {prompt}")

    try:
        # Create a chat completion request
        chat_completion = client.chat.completions.create(
            model="tgi",
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}\nPlease provide complete, runnable Manim code."
                }
            ],
            max_tokens=4096,  # Maximum allowed tokens
            stream=True
        )

        # Collect the complete response
        full_response = ""
        print("\nResponse:")
        for message in chat_completion:
            if message.choices[0].delta.content:
                content = message.choices[0].delta.content
                full_response += content
                print(content, end="", flush=True)

        print("\n")

        # Generate video from the code
        if full_response:
            video_path = generate_video_from_code(full_response)
            if video_path:
                print(f"\nVideo generated successfully at: {video_path}")
            else:
                print("\nFailed to generate video")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    animation_prompt = "Create a manim animation of a transformer architecture"
    generate_animation_code(animation_prompt)