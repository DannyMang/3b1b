# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("haidangung/qwen3-manim-16bit")
model = AutoModelForCausalLM.from_pretrained(
    "haidangung/qwen3-manim-16bit",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32, # Use float16 if CUDA is available
    device_map="auto" if torch.cuda.is_available() else None # Automatically map to GPU if available
)

def generate_response(messages, max_new_tokens=512):
    # Apply chat template
    # The Qwen3 notebook (lines 1471-1476) uses apply_chat_template
    # It's good practice to check if it exists, similar to test/huggingface_test.py (lines 15-22)
    if hasattr(tokenizer, 'apply_chat_template'):
        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
    else:
        # Fallback for models without a chat template
        prompt = ""
        for message in messages:
            prompt += f"{message['role']}: {message['content']}\n"
        prompt += "assistant: " # Or the appropriate turn indicator for your model

    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt")

    # Move inputs to the same device as the model
    if torch.cuda.is_available():
        inputs = inputs.to(model.device)

    # Generate response
    # Generation parameters can be tuned, see test/test.py (lines 91-99)
    # or the Qwen3 notebook (lines 1479-1484)
    with torch.no_grad(): # Important for inference to save memory and compute
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,       # Controls randomness. Lower is more deterministic.
            top_p=0.9,             # Nucleus sampling: considers the smallest set of tokens whose cumulative probability exceeds top_p.
            do_sample=True,        # Whether to use sampling; must be True for temperature and top_p to have an effect.
            pad_token_id=tokenizer.eos_token_id # Set pad_token_id to eos_token_id for open-end generation
        )

    # Decode the generated tokens
    # The slicing removes the input prompt from the generated output.
    response_text = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    return response_text

if __name__ == '__main__':
    # Example usage:
    user_prompt = "Write a Manim scene that animates the formula e^{i\pi} + 1 = 0."
    messages = [
        {"role": "user", "content": user_prompt}
    ]

    print(f"User: {user_prompt}")
    assistant_response = generate_response(messages)
    print(f"Assistant: {assistant_response}")

    # Example of a follow-up
    messages.append({"role": "assistant", "content": assistant_response})
    follow_up_prompt = "Can you make the animation more visually appealing with colors?"
    messages.append({"role": "user", "content": follow_up_prompt})

    print(f"\nUser: {follow_up_prompt}")
    assistant_response_2 = generate_response(messages)
    print(f"Assistant: {assistant_response_2}")

