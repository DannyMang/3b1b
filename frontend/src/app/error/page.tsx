"use client";
import React from "react";
import Link from "next/link";
import MathAnimationCanvas from "@/components/MathAnimationCanvas";

export default function ErrorPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <div className="w-full max-w-5xl flex flex-col md:flex-row rounded-2xl shadow-2xl overflow-hidden border border-neutral-800 bg-neutral-900">
        {/* Left: Error message */}
        <div className="flex-1 flex flex-col justify-center px-8 py-12 md:px-12">
          <div className="flex flex-col gap-6 max-w-sm mx-auto w-full">
            <h1 className="text-2xl font-bold mb-2">Oops! Something went wrong</h1>
            <div className="p-4 rounded-lg bg-red-500/10 border border-red-500 text-red-500">
              <p className="text-sm">We encountered an error while processing your request.</p>
            </div>
            <div className="flex flex-col gap-4">
              <p className="text-neutral-400 text-sm">
                This could be due to:
              </p>
              <ul className="list-disc list-inside text-neutral-400 text-sm space-y-2">
                <li>Invalid or expired authentication link</li>
                <li>Network connectivity issues</li>
                <li>Server-side error</li>
              </ul>
            </div>
            <div className="flex flex-col gap-4 mt-4">
              <Link 
                href="/signin" 
                className="w-full py-2 rounded-lg bg-blue-500 text-white font-semibold hover:bg-blue-600 transition text-center"
              >
                Return to Sign In
              </Link>
              <Link 
                href="/" 
                className="w-full py-2 rounded-lg border border-neutral-700 bg-black text-white font-semibold hover:bg-neutral-800 transition text-center"
              >
                Go to Homepage
              </Link>
            </div>
          </div>
        </div>
        {/* Right: Math animation background */}
        <div className="hidden md:flex flex-1 items-center justify-center relative overflow-hidden">
          <MathAnimationCanvas variant="paraboloid" />
        </div>
      </div>
    </div>
  );
} 