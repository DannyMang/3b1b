generative coding model trained to ONLY generate 3B1B videos using https://github.com/DannyMang/3b1b library!

update: we will use community edition found at https://github.com/ManimCommunity/manim/ since community version looks more polished

Current Achievements:
- Have first finetuned model @ https://huggingface.co/haidangung/qwen3-manim-16bit
- LoRA weights can be found @ https://huggingface.co/haidangung/qwen3-manim-lora

Current tasks:
- Have not tested how good current finetuned model is, what ways can I measure performance metrics of model?
    - Create a standardized prompt set covering various mathematical visualization scenarios: basic geometric operations, function plotting, algebraic manipulations, and complex mathematical proofs. Test your fine-tuned model alongside GPT-4, Claude, and other code generation models to quantify improvement areas.

    The evaluation script should capture multiple success criteria: compilation success rate, visual output accuracy, code elegance, and execution efficiency. This multi-dimensional assessment will provide insights into where your specialized fine-tuning delivers advantages over general-purpose models and identify specific weaknesses requiring targeted improvement.
- Need to re finetune or some other method to align model to do task given and not irrelevant tasks
- Clean up dataset?
- ensure output has working code


- ALL OF GRANT"S VIDEO CODE CAN BE FOUND : https://github.com/3b1b/videos

# April 28, 2025
- lets try finetuning a model to see how good it performs 

# May 3
- came across https://github.com/unslothai/unsloth, we're gna use this to finetune efficiently:
- relevant resources https://docs.unsloth.ai/basics/qwen3-how-to-run-and-fine-tune#fine-tuning-qwen3-with-unsloth
- https://docs.unsloth.ai/basics/datasets-guide
- https://docs.unsloth.ai/get-started/fine-tuning-guide

- current goal build dataset to finetune on 
- we will be using qwen 3, 14b just because alibaba >

# May 12

overview of plans:
1. Modern Serverless Architecture?
[User Interface] → [API Gateway] → [Authentication Service] → [LLM Service] → [Rendering Service]
                                                           ↓
                           [Database] ← [Payment Processing] → [User Management]
Key Components:

Frontend: React/Next.js application hosted on Vercel or Netlify
API Gateway: AWS API Gateway or Cloudflare Workers
Authentication: Auth0 or Supabase for secure user authentication
LLM Service: Containerized Qwen3 model on AWS ECS/EKS or GCP Cloud Run
Rendering Service: Service that takes generated Manim code and renders videos
Database: MongoDB or PostgreSQL for storing user data and generated content
Payment Processing: Stripe for handling subscriptions and one-time purchases

2. Security Measures
Input Validation: Implement strict validation of user inputs to prevent prompt injection attacks
Rate Limiting: Limit API calls per user to prevent abuse
Content Filtering: Filter both input prompts and model outputs for inappropriate content
Output Sanitization: Validate and sanitize generated code before execution
Encryption: Use TLS for data in transit and encryption for data at rest
Authentication: Implement robust OAuth or JWT-based authentication
Monitoring: Set up logging and real-time monitoring to detect unusual patterns
Regular Audits: Conduct security audits of your infrastructure

UX/UI Design for Your Target Audiences
Product will serve two main audiences:
1. Developers

Key UX Elements:

Clean, minimalist interface with code view options
Detailed API documentation with examples
Option to customize parameters (temperature, etc.)
Code export functionality with different format options
Git integration for version control of animations

2. Educators/Teachers
Educators want simplicity, visual feedback, and educational value.
Key UX Elements:

Guided wizard interface with templates
Visual preview of animations in real-time where possible
Curriculum integration examples
Ability to save and organize projects by subject/lesson
Collaboration features for team teaching
Export formats compatible with classroom presentation software

Technical Implementation Roadmap
Phase 1: MVP (2-3 months)

Deploy Qwen3 model with basic prompting
Build simple web UI for text-to-animation generation
Implement basic user authentication
Set up simple payment processing with Stripe
Develop basic animation rendering pipeline

Phase 2: Enhancement (2-3 months)

Improve model fine-tuning with user feedback
Build API for developer access
Add more animation templates and examples
Implement more robust security measures
Develop education-specific features

Phase 3: Scaling (2-3 months)

Optimize infrastructure for cost and performance
Implement advanced analytics
Build collaboration features
Develop integration plugins for common education platforms
Expand marketing and partnership efforts

Technology Stack Recommendations
Frontend

Framework: Next.js with TypeScript
UI Library: Tailwind CSS + Shadcn UI
State Management: Zustand or Redux Toolkit
Animation Preview: Three.js or custom WebGL renderer

Backend

API: Node.js with Express or FastAPI with Python
LLM Deployment: Docker + Kubernetes or serverless options like AWS Lambda
Database: MongoDB for flexibility or PostgreSQL for relational data
Caching: Redis for performance optimization
Video Processing: FFmpeg for video generation

Infrastructure

Cloud Provider: AWS, GCP, or Azure
CI/CD: GitHub Actions or GitLab CI
Monitoring: Datadog or Prometheus + Grafana
Security: AWS WAF, CloudFlare, or Akamai
