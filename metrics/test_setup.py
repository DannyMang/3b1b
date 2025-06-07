import os
from dotenv import load_dotenv
from openai import OpenAI

def test_environment_setup():
    """Test that all required environment variables and dependencies are available"""
    print("🔍 Testing Model Evaluation Setup")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv('.env.local')
    
    # Check required environment variables
    required_vars = {
        'OPENROUTER_API_KEY': 'OpenRouter API (for GPT-4, Claude, Gemini)',
        'HUGGINGFACE_BASE_URL': 'HuggingFace Endpoint (for your fine-tuned model)',
        'HUGGINGFACE_API_KEY': 'HuggingFace API Key (for your fine-tuned model)'
    }
    
    print("📋 Environment Variables:")
    all_vars_present = True
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask the key for security
            masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"   ✅ {var}: {masked_value} ({description})")
        else:
            print(f"   ❌ {var}: Missing ({description})")
            all_vars_present = False
    
    if not all_vars_present:
        print("\n❌ Missing environment variables. Please check your .env.local file.")
        return False
    
    # Test OpenRouter connection
    print("\n🌐 Testing API Connections:")
    
    try:
        openrouter_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv('OPENROUTER_API_KEY')
        )
        
        # Simple test call
        response = openrouter_client.chat.completions.create(
            model="openai/gpt-3.5-turbo",  # Use cheaper model for testing
            messages=[{"role": "user", "content": "Hello, just testing connection!"}],
            max_tokens=10
        )
        
        print("   ✅ OpenRouter: Connected successfully")
        
    except Exception as e:
        print(f"   ❌ OpenRouter: Connection failed - {str(e)}")
        return False
    
    # Test HuggingFace connection
    try:
        hf_client = OpenAI(
            base_url=os.getenv('HUGGINGFACE_BASE_URL'),
            api_key=os.getenv('HUGGINGFACE_API_KEY')
        )
        
        # Simple test call
        response = hf_client.chat.completions.create(
            model="tgi",
            messages=[{"role": "user", "content": "Test connection"}],
            max_tokens=10
        )
        
        print("   ✅ HuggingFace: Connected successfully")
        
    except Exception as e:
        print(f"   ❌ HuggingFace: Connection failed - {str(e)}")
        print("      Note: This is expected if your model isn't currently running")
    
    # Test dataset file
    print("\n📊 Testing Dataset:")
    dataset_path = "metrics/evaluation_dataset_complete.json"
    
    if os.path.exists(dataset_path):
        try:
            import json
            with open(dataset_path, 'r') as f:
                data = json.load(f)
            print(f"   ✅ Dataset: Found {len(data['queries'])} evaluation prompts")
        except Exception as e:
            print(f"   ❌ Dataset: File exists but can't be read - {str(e)}")
            return False
    else:
        print(f"   ❌ Dataset: File not found at {dataset_path}")
        print("      Run: python metrics/metric_dataset.py")
        return False
    
    # Test dependencies
    print("\n📦 Testing Dependencies:")
    
    required_packages = ['openai', 'pandas', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}: Installed")
        except ImportError:
            print(f"   ❌ {package}: Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("\n🎉 Setup Test Complete!")
    print("=" * 50)
    print("✅ All systems ready for model evaluation!")
    print("\nNext steps:")
    print("1. Run: python model_evaluator.py")
    print("2. Choose option 2 for test evaluation (10 prompts)")
    print("3. If successful, run full evaluation with option 1")
    
    return True

def test_single_model_call():
    """Test a single model call to verify everything works"""
    print("\n🧪 Testing Single Model Call")
    print("-" * 30)
    
    load_dotenv('.env.local')
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv('OPENROUTER_API_KEY')
        )
        
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{
                "role": "user", 
                "content": "Create a simple Manim animation showing a circle. Please provide complete, runnable Manim code."
            }],
            max_tokens=200
        )
        
        print("✅ Test call successful!")
        print(f"Response preview: {response.choices[0].message.content[:150]}...")
        
    except Exception as e:
        print(f"❌ Test call failed: {e}")

if __name__ == "__main__":
    success = test_environment_setup()
    
    if success:
        # Run a single test call
        test_single_model_call()
    else:
        print("\n⚠️  Please fix the issues above before running the full evaluation.") 