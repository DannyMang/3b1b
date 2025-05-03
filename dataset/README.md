# Dataset Format for Fine-tuning

## Alpaca-style Format

The dataset should be in JSON format with the following structure:

```json
{
    "instruction": "Create a circle that transforms into a square",
    "input": "",  // Optional context or additional information
    "output": "from manim import *\n\nclass GeneratedScene(Scene):\n    def construct(self):\n        circle = Circle()\n        square = Square()\n        self.play(Create(circle))\n        self.play(Transform(circle, square))"
}
```

### Fields:
- `instruction`: Natural language description of the animation
- `input`: (Optional) Additional context or parameters
- `output`: The corresponding Manim code that creates the animation

### Example Dataset Entry:
```json
{
    "instruction": "Show a bouncing ball with gravity",
    "input": "ball_color: RED, gravity: 9.8",
    "output": "from manim import *\n\nclass BouncingBall(Scene):\n    def construct(self):\n        ball = Circle(radius=0.5, color=RED)\n        self.play(Create(ball))\n        self.play(ball.animate.shift(DOWN * 2), rate_func=rate_functions.ease_in_out)"
}
```

Store your dataset in `dataset/train.json` and `dataset/validation.json` for training and validation respectively.
