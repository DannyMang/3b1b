"use client";
import React from "react";
import Link from "next/link";
import MathAnimationCanvas from "@/components/MathAnimationCanvas";

export default function ConfirmSignUpPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <div className="w-full max-w-5xl flex flex-col md:flex-row rounded-2xl shadow-2xl overflow-hidden border border-neutral-800 bg-neutral-900">
        {/* Left: Confirmation message */}
        <div className="flex-1 flex flex-col justify-center px-8 py-12 md:px-12">
          <div className="flex flex-col gap-6 max-w-sm mx-auto w-full">
            <div className="flex items-center justify-center w-12 h-12 rounded-full bg-green-500/10 mb-4">
              <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h1 className="text-2xl font-bold text-center">Check your email</h1>
            <p className="text-neutral-400 text-center">
              We've sent you an email with a link to confirm your account. Please check your inbox and follow the instructions to complete your registration.
            </p>
            <div className="mt-6 text-sm text-neutral-400 text-center">
              <p>Didn't receive the email?</p>
              <ul className="mt-2 space-y-2">
                <li>• Check your spam folder</li>
                <li>• Make sure you entered the correct email address</li>
                <li>• Wait a few minutes and try again</li>
              </ul>
            </div>
            <div className="mt-6 flex flex-col gap-3">
              <Link
                href="/signin"
                className="w-full py-2 rounded-lg bg-white text-black font-semibold hover:bg-neutral-200 transition text-center"
              >
                Return to Sign In
              </Link>
              <Link
                href="/"
                className="w-full py-2 rounded-lg border border-neutral-700 text-white font-semibold hover:bg-neutral-800 transition text-center"
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