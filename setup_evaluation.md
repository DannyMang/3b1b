# Model Evaluation Setup Instructions

This guide helps you set up the comprehensive model evaluation system to compare your fine-tuned Manim model against leading AI models.

## 🔧 Environment Setup

### 1. Create `.env.local` file

Create a `.env.local` file in the `3b1b/` directory with the following variables:

```bash
# Your existing HuggingFace configuration
HUGGINGFACE_BASE_URL=your_huggingface_endpoint
HUGGINGFACE_API_KEY=your_huggingface_api_key

# OpenRouter API for accessing GPT-4, Claude, Gemini
OPENROUTER_API_KEY=your_openrouter_api_key
```

### 2. Get OpenRouter API Key

1. Go to [OpenRouter.ai](https://openrouter.ai)
2. Sign up for an account
3. Navigate to the API Keys section
4. Create a new API key
5. Add it to your `.env.local` file

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Running the Evaluation

### Option 1: Test Evaluation (10 prompts)
Perfect for testing your setup:

```bash
python model_evaluator.py
# Select option 2 when prompted
```

### Option 2: Full Evaluation (200 prompts) 
Complete evaluation across all categories:

```bash
python model_evaluator.py
# Select option 1 when prompted
```

## 📊 Models Being Tested

The system will test these models:

1. **Your Fine-tuned Model**: `fine_tuned_manim`
   - Your custom Manim code generation model
   
2. **GPT-4o**: `gpt4o` 
   - OpenAI's latest model via OpenRouter
   
3. **Claude 3.5 Sonnet**: `claude_sonnet`
   - Anthropic's Claude via OpenRouter
   
4. **Gemini Pro 1.5**: `gemini_pro`
   - Google's Gemini via OpenRouter
   
5. **Llama 3.1 405B**: `llama_405b`
   - Meta's largest Llama model via OpenRouter

## 📈 Evaluation Categories

Your models will be tested across:

- **Basic Geometry** (25 prompts): Pentagon construction, Pythagorean theorem, etc.
- **Function Plotting** (25 prompts): Taylor series, derivatives, limits
- **Linear Algebra** (25 prompts): Matrix operations, eigenvalues
- **Calculus Concepts** (25 prompts): Green's theorem, differential equations
- **Probability/Statistics** (20 prompts): Central limit theorem, Bayes
- **Number Theory** (20 prompts): Prime proofs, modular arithmetic
- **Machine Learning** (20 prompts): Neural networks, gradient descent
- **Advanced Topics** (20 prompts): Fractals, chaos theory, topology
- **Inappropriate Topics** (20 prompts): Tests domain focus

## 📋 Results Analysis

After running evaluation:

```bash
python results_analyzer.py
```

This will generate:
- Detailed comparison report
- Success rates by model and category
- Code quality analysis
- CSV export for further analysis

## 💡 Expected Output Files

- `evaluation_results_YYYYMMDD_HHMMSS.json`: Raw results
- `evaluation_results_YYYYMMDD_HHMMSS_report.txt`: Analysis report
- `evaluation_results_YYYYMMDD_HHMMSS_detailed.csv`: CSV for spreadsheets

## 🎯 Key Metrics

The evaluation measures:

1. **Success Rate**: How often models generate valid responses
2. **Code Quality**: Proper Manim imports, Scene classes, construct methods
3. **Domain Focus**: How well models refuse inappropriate requests
4. **Category Performance**: Strengths/weaknesses across math topics
5. **Response Quality**: Length, keyword usage, structure

## ⚠️ Important Notes

- **Rate Limiting**: Built-in delays between API calls
- **Cost Awareness**: OpenRouter charges per token - test with 10 prompts first
- **Intermediate Saves**: Results saved every 10 prompts (recoverable if interrupted)
- **Error Handling**: Individual failures won't stop the entire evaluation

## 🔍 Troubleshooting

**Missing API Keys**: Check `.env.local` file exists and has correct keys
**Import Errors**: Run `pip install -r requirements.txt`
**Rate Limits**: Increase delays in `model_evaluator.py` if needed
**No Results**: Ensure `metrics/evaluation_dataset_complete.json` exists

## 🎊 Ready to Evaluate!

Your fine-tuned Manim model is ready for comprehensive evaluation against the world's leading AI models. This will give you concrete data on:

- How your specialized model compares to general-purpose models
- Which mathematical topics your model handles best
- Whether your model maintains appropriate domain focus
- Areas for potential improvement in your fine-tuning

Good luck with your evaluation! 🚀 