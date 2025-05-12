import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ChevronRight, Code, Lightbulb, Play, Sigma, Sparkles, Zap } from "lucide-react"
import AnimatedMathBackground from "@/components/AnimatedMathBackground"

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col dark bg-black text-white">
      <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center space-x-4 sm:justify-between sm:space-x-0">
          <div className="flex gap-2 items-center text-xl font-bold">
            <Sigma className="h-6 w-6 text-primary" />
            <span>Text2Manim</span>
          </div>
          <div className="flex flex-1 items-center justify-end space-x-4">
            <nav className="flex items-center space-x-2">
              <Link
                href="#features"
                className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
              >
                Features
              </Link>
              <Link
                href="#how-it-works"
                className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
              >
                How It Works
              </Link>
              <Link
                href="#docs"
                className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
              >
                Docs
              </Link>
              <Link href="/signin">
                <Button variant="default" size="sm">
                  Get Started
                </Button>
              </Link>
            </nav>
          </div>
        </div>
      </header>
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48 relative overflow-hidden bg-black">
          <AnimatedMathBackground />
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-[1fr_400px] lg:gap-12 xl:grid-cols-[1fr_600px]">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none text-blue-400">
                    Transform Text to Beautiful Math Animations
                  </h1>
                  <p className="max-w-[600px] text-muted-foreground md:text-xl">
                    Create stunning mathematical animations like 3Blue1Brown with simple text commands. No coding
                    required.
                  </p>
                </div>
                <div className="flex flex-col gap-2 min-[400px]:flex-row">
                  <Button className="inline-flex items-center">
                    Try It Now
                    <ChevronRight className="ml-1 h-4 w-4" />
                  </Button>
                  <Button variant="outline" className="inline-flex items-center">
                    View Documentation
                  </Button>
                </div>
                <div className="flex items-center space-x-4 text-sm">
                  <div className="flex items-center space-x-1">
                    <Zap className="h-4 w-4" />
                    <span>Fast Rendering</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Code className="h-4 w-4" />
                    <span>Simple Syntax</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-center">
                <div className="relative w-full max-w-[600px] overflow-hidden rounded-lg border bg-background p-2 shadow-xl">
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 opacity-20 blur-3xl"></div>
                  <div className="relative aspect-video overflow-hidden rounded-md bg-black">
                    <div className="flex h-full w-full items-center justify-center">
                      <div className="text-center">
                        <Play className="mx-auto h-16 w-16 text-white opacity-80" />
                        <p className="mt-4 text-white">Your Manim Demo Video</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="demo" className="w-full py-12 md:py-24 lg:py-32 bg-black">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <div className="inline-flex items-center rounded-lg bg-blue-100 px-3 py-1 text-sm">
                  <Play className="mr-1 h-4 w-4" />
                  <span>See It In Action</span>
                </div>
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-blue-400">
                  Watch Text2Manim Transform Your Ideas
                </h2>
                <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  From simple text commands to beautiful mathematical animations in seconds
                </p>
              </div>
            </div>
            <div className="mx-auto mt-12 max-w-5xl">
              <div className="overflow-hidden rounded-xl border bg-background shadow-xl">
                <div className="aspect-video w-full bg-black">
                  <div className="flex h-full w-full items-center justify-center">
                    <div className="text-center">
                      <Play className="mx-auto h-24 w-24 text-white opacity-80" />
                      <p className="mt-4 text-xl text-white">Your Featured Demo Video</p>
                      <p className="mt-2 text-sm text-gray-400">Replace this with your actual Manim demonstration</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="features" className="w-full py-12 md:py-24 lg:py-32 bg-black">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-blue-400">Powerful Features</h2>
                <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Everything you need to create stunning mathematical animations
                </p>
              </div>
            </div>
            <div className="mx-auto grid max-w-5xl items-center gap-6 py-12 lg:grid-cols-3 lg:gap-12">
              <div className="flex flex-col justify-center space-y-4 rounded-lg border bg-background p-6 shadow-sm">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
                  <Lightbulb className="h-6 w-6 text-blue-600" />
                </div>
                <div className="space-y-2">
                  <h3 className="text-xl font-bold">Simple Text Commands</h3>
                  <p className="text-muted-foreground">
                    Write natural language descriptions that automatically convert to Manim animations
                  </p>
                </div>
              </div>
              <div className="flex flex-col justify-center space-y-4 rounded-lg border bg-background p-6 shadow-sm">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
                  <Sigma className="h-6 w-6 text-blue-600" />
                </div>
                <div className="space-y-2">
                  <h3 className="text-xl font-bold">Mathematical Precision</h3>
                  <p className="text-muted-foreground">
                    Render complex equations, graphs, and geometric transformations with perfect accuracy
                  </p>
                </div>
              </div>
              <div className="flex flex-col justify-center space-y-4 rounded-lg border bg-background p-6 shadow-sm">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
                  <Zap className="h-6 w-6 text-blue-600" />
                </div>
                <div className="space-y-2">
                  <h3 className="text-xl font-bold">Fast Rendering</h3>
                  <p className="text-muted-foreground">
                    Generate high-quality animations in a fraction of the time of traditional methods
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="how-it-works" className="w-full py-12 md:py-24 lg:py-32 bg-black">
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-2 lg:gap-12">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <div className="inline-flex items-center rounded-lg bg-blue-100 px-3 py-1 text-sm">
                    <Code className="mr-1 h-4 w-4" />
                    <span>How It Works</span>
                  </div>
                  <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-blue-400">
                    From Text to Animation in 3 Simple Steps
                  </h2>
                  <p className="max-w-[600px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                    Our advanced AI understands your mathematical intent and generates beautiful animations
                  </p>
                </div>
                <div className="space-y-4">
                  <div className="flex items-start space-x-4">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-900">
                      1
                    </div>
                    <div className="space-y-1">
                      <h3 className="text-xl font-bold">Write Your Description</h3>
                      <p className="text-muted-foreground">
                        Describe the mathematical concept or animation you want to create in plain text
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-900">
                      2
                    </div>
                    <div className="space-y-1">
                      <h3 className="text-xl font-bold">AI Conversion</h3>
                      <p className="text-muted-foreground">
                        Our system interprets your text and generates the appropriate Manim code
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-900">
                      3
                    </div>
                    <div className="space-y-1">
                      <h3 className="text-xl font-bold">Render and Export</h3>
                      <p className="text-muted-foreground">
                        Get a high-quality animation ready to use in your presentations, videos, or educational content
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-center">
                <div className="relative w-full max-w-[500px] overflow-hidden rounded-lg border bg-background p-4 shadow-xl">
                  <div className="space-y-4">
                    <div className="rounded-md bg-muted p-3 font-mono text-sm">
                      <div className="text-green-500"># Input text:</div>
                      <div className="mt-2">
                        {
                          "Create an animation showing a circle transforming into a square while demonstrating the concept of area preservation"
                        }
                      </div>
                      <div className="mt-4 text-blue-500"># Generated Manim code:</div>
                      <div className="mt-2 text-xs text-muted-foreground">
                        {`class CircleToSquare(Scene):`}
                        <br />
                        {`    def construct(self):`}
                        <br />
                        {`        circle = Circle()`}
                        <br />
                        {`        square = Square()`}
                        <br />
                        {`        self.play(Transform(circle, square, run_time=2))`}
                        <br />
                        {`        self.wait()`}
                      </div>
                    </div>
                    <div className="aspect-video rounded-md bg-black">
                      <div className="flex h-full w-full items-center justify-center">
                        <div className="text-center">
                          <p className="text-white">Animation Output</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="w-full py-12 md:py-24 lg:py-32 bg-black">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-blue-400">
                  Ready to Create Beautiful Math Animations?
                </h2>
                <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Join thousands of educators, content creators, and math enthusiasts
                </p>
              </div>
              <div className="flex flex-col gap-2 min-[400px]:flex-row">
                <Button size="lg" className="inline-flex items-center">
                  Get Started for Free
                  <ChevronRight className="ml-1 h-4 w-4" />
                </Button>
                <Button variant="outline" size="lg" className="inline-flex items-center">
                  View Documentation
                </Button>
              </div>
            </div>
          </div>
        </section>
      </main>
      <footer className="w-full border-t bg-background py-6">
        <div className="container flex flex-col items-center justify-between gap-4 md:flex-row md:gap-0">
          <div className="flex items-center gap-2 text-lg font-semibold">
            <Sigma className="h-5 w-5 text-primary" />
            <span>Text2Manim</span>
          </div>
          <p className="text-center text-sm text-muted-foreground md:text-left">
            © {new Date().getFullYear()} made with ❤️ by <a href="https://x.com/danielung19" target="_blank" rel="noopener noreferrer">daniel ung</a>
          </p>
          <div className="flex gap-4">
            <Link href="#" className="text-sm text-muted-foreground hover:text-foreground">
              Terms 
            </Link>
            <Link href="#" className="text-sm text-muted-foreground hover:text-foreground">
              Privacy
            </Link>
            <Link href="#" className="text-sm text-muted-foreground hover:text-foreground">
              Contact
            </Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
