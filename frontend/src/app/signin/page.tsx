"use client";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import MathAnimationCanvas from "@/components/MathAnimationCanvas";
import { createClient } from "@/utils/supabase/client";
import { useRouter } from "next/navigation";

const prompts = [
  "Visualize a Fourier series",
  "Show a 3D rotation matrix",
  "Animate a Taylor expansion",
  "Plot a Mandelbrot set",
  "What is a Lissajous curve?",
  "Draw a Sierpinski triangle",
  "Simulate a random walk",
  "Graph a complex function",
  "Show eigenvectors in action",
  "Animate a double pendulum",
];

function useTypingEffect(strings: string[], typingSpeed = 60, pause = 1200, backspaceSpeed = 30, pauseBetween = 600) {
  const [display, setDisplay] = useState("");
  const [index, setIndex] = useState(0);
  const [typing, setTyping] = useState(true);

  useEffect(() => {
    let timeout: NodeJS.Timeout;
    const current = strings[index];
    if (typing) {
      if (display.length < current.length) {
        timeout = setTimeout(() => setDisplay(current.slice(0, display.length + 1)), typingSpeed);
      } else {
        timeout = setTimeout(() => setTyping(false), pause);
      }
    } else {
      if (display.length > 0) {
        timeout = setTimeout(() => setDisplay(current.slice(0, display.length - 1)), backspaceSpeed);
      } else {
        timeout = setTimeout(() => {
          setTyping(true);
          setIndex((i) => (i + 1) % strings.length);
        }, pauseBetween);
      }
    }
    return () => clearTimeout(timeout);
  }, [display, typing, index, strings, typingSpeed, pause, backspaceSpeed, pauseBetween]);

  return display;
}

export default function SignInPage() {
  const router = useRouter();
  const typedPrompt = useTypingEffect(prompts);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [supabase, setSupabase] = useState<any>(null);

  useEffect(() => {
    const initSupabase = async () => {
      const client = await createClient();
      setSupabase(client);
    };
    initSupabase();
  }, []);

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!supabase) return;
    
    setLoading(true);
    setError(null);

    try {
      const { error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) throw error;
      router.push("/");
      router.refresh();
    } catch (error) {
      setError(error instanceof Error ? error.message : "An error occurred during sign in");
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
    if (!supabase) return;
    
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: "google",
        options: {
          redirectTo: `${window.location.origin}/auth/callback`,
        },
      });
      if (error) throw error;
    } catch (error) {
      setError(error instanceof Error ? error.message : "An error occurred during Google sign in");
    }
  };

  const handleGithubSignIn = async () => {
    if (!supabase) return;
    
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: "github",
        options: {
          redirectTo: `${window.location.origin}/auth/callback`,
        },
      });
      if (error) throw error;
    } catch (error) {
      setError(error instanceof Error ? error.message : "An error occurred during GitHub sign in");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <div className="w-full max-w-5xl flex flex-col md:flex-row rounded-2xl shadow-2xl overflow-hidden border border-neutral-800 bg-neutral-900">
        {/* Left: Sign in form */}
        <div className="flex-1 flex flex-col justify-center px-8 py-12 md:px-12">
          <div className="flex flex-col gap-6 max-w-sm mx-auto w-full">
            <h1 className="text-2xl font-bold mb-2">Sign in to Text2Manim</h1>
            {error && (
              <div className="p-3 rounded-lg bg-red-500/10 border border-red-500 text-red-500 text-sm">
                {error}
              </div>
            )}
            <button
              onClick={handleGoogleSignIn}
              className="w-full flex items-center justify-center gap-2 py-2 rounded-lg border border-neutral-700 bg-black text-white font-semibold hover:bg-neutral-800 transition"
            >
              <svg className="w-5 h-5" viewBox="0 0 48 48">
                <g>
                  <path fill="#fff" d="M44.5 20H24v8.5h11.7C34.7 33.1 30.1 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c2.6 0 5 .8 7 2.3l6.4-6.4C33.5 5.1 28.1 3 24 3 12.4 3 3 12.4 3 24s9.4 21 21 21c10.5 0 20-7.5 20-21 0-1.3-.1-2.7-.5-4z"/>
                </g>
              </svg>
              Continue with Google
            </button>
            <button
              onClick={handleGithubSignIn}
              className="w-full flex items-center justify-center gap-2 py-2 rounded-lg border border-neutral-700 bg-black text-white font-semibold hover:bg-neutral-800 transition"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path fill="currentColor" d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.014-1.703-2.782.604-3.369-1.342-3.369-1.342-.454-1.154-1.11-1.461-1.11-1.461-.908-.62.069-.608.069-.608 1.004.07 1.532 1.032 1.532 1.032.892 1.529 2.341 1.088 2.91.832.092-.646.35-1.088.636-1.339-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.272.098-2.65 0 0 .84-.269 2.75 1.025A9.564 9.564 0 0 1 12 6.844c.85.004 1.705.115 2.504.337 1.909-1.294 2.748-1.025 2.748-1.025.546 1.378.202 2.397.1 2.65.64.699 1.028 1.592 1.028 2.683 0 3.842-2.338 4.687-4.566 4.936.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.744 0 .267.18.577.688.479C19.138 20.163 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
              </svg>
              Continue with GitHub
            </button>
            <div className="flex items-center my-4">
              <div className="flex-grow h-px bg-neutral-700" />
              <span className="mx-3 text-neutral-500 text-xs">OR</span>
              <div className="flex-grow h-px bg-neutral-700" />
            </div>
            <form onSubmit={handleSignIn} className="w-full flex flex-col gap-3">
              <label className="text-sm font-medium" htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
                className="w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
              <label className="text-sm font-medium" htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                className="w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
                minLength={6}
              />
              <button
                type="submit"
                disabled={loading}
                className="w-full py-2 mt-2 rounded-lg bg-blue-500 text-white font-semibold hover:bg-blue-600 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? "Signing in..." : "Sign in"}
              </button>
            </form>
            <div className="mt-6 text-sm text-neutral-400 text-center">
              Don&apos;t have an account? <Link href="/signup" className="text-blue-400 hover:underline">Sign up</Link>
            </div>
          </div>
        </div>
        {/* Right: Math animation background */}
        <div className="hidden md:flex flex-1 items-center justify-center relative overflow-hidden">
          <MathAnimationCanvas variant="paraboloid" />
          <div className="relative z-10 flex flex-col items-center justify-center w-full h-full">
            <div className="bg-white/90 rounded-xl px-6 py-4 flex items-center gap-3 shadow-lg">
              <input
                className="bg-transparent border-none outline-none text-black text-lg placeholder:text-neutral-400 w-full overflow-x-auto text-nowrap pr-2"
                value={typedPrompt}
                readOnly
              />
              <button className="rounded-full bg-blue-600 p-2 text-white hover:bg-blue-700 transition">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14m-7-7l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 