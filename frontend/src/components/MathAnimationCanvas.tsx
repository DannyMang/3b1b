"use client";

import React, { useRef, useEffect, useState } from "react";

export type MathAnimationVariant = "paraboloid" | "lorenz";

interface MathAnimationCanvasProps {
  variant?: MathAnimationVariant;
}

export default function MathAnimationCanvas({ variant = "paraboloid" }: MathAnimationCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const headPositionRef = useRef<number>(0);
  const velocityRef = useRef<number>(1);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;

    function resize() {
      if (!canvas) return;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;
      const rect = canvas.parentElement?.getBoundingClientRect();
      const width = rect?.width || 600;
      const height = rect?.height || 600;
      let dpr = window.devicePixelRatio || 1;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function drawParaboloid(time: number) {
      resize();
      if (!canvas) return;
      const rect = canvas.parentElement?.getBoundingClientRect();
      const width = rect?.width || 600;
      const height = rect?.height || 600;
      if (!ctx) return;
      ctx.clearRect(0, 0, width, height);
      ctx.save();
      ctx.globalAlpha = 0.9;
      ctx.fillStyle = "#181926";
      ctx.fillRect(0, 0, width, height);
      ctx.restore();

      // 3D projection helpers
      function project3D([x, y, z]: [number, number, number], angle = Math.PI / 5) {
        // Simple isometric projection
        const scale = Math.min(width, height) * 0.18;
        const px = width / 2 + (x - z) * Math.cos(angle) * scale;
        const py = height / 2 + (y - (x + z) * Math.sin(angle) * 0.5) * scale;
        return [px, py];
      }

      // Draw paraboloids
      ctx.save();
      ctx.globalAlpha = 0.18;
      for (let sign of [1, -1]) {
        for (let x = -1.5; x <= 1.5; x += 0.05) {
          ctx.beginPath();
          for (let z = -1.5; z <= 1.5; z += 0.05) {
            const y = sign * x * x;
            const [px, py] = project3D([x, y, z]);
            if (z === -1.5) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
          }
          ctx.strokeStyle = sign === 1 ? "#60a5fa" : "#f472b6";
          ctx.lineWidth = 2;
          ctx.stroke();
        }
      }
      ctx.restore();

      // Draw spiraling circle
      const spiralT = (time * 0.0005) % 1;
      const spiralAngle = spiralT * 2 * Math.PI * 3;
      const spiralRadius = 1.2 - spiralT * 1.2;
      const spiralY = Math.cos(spiralT * Math.PI) * 1.2;
      const spiralX = Math.cos(spiralAngle) * spiralRadius;
      const spiralZ = Math.sin(spiralAngle) * spiralRadius;
      const [cx, cy] = project3D([spiralX, spiralY, spiralZ]);
      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, 18, 0, 2 * Math.PI);
      ctx.fillStyle = "#fbbf24";
      ctx.shadowColor = "#fbbf24";
      ctx.shadowBlur = 24;
      ctx.globalAlpha = 0.85;
      ctx.fill();
      ctx.restore();
    }

    function drawLorenz(time: number) {
      resize();
      if (!canvas) return;
      const rect = canvas.parentElement?.getBoundingClientRect();
      const width = rect?.width || 600;
      const height = rect?.height || 600;
      if (!ctx) return;
      ctx.clearRect(0, 0, width, height);
      ctx.save();
      ctx.globalAlpha = 0.9;
      ctx.fillStyle = "#181926";
      ctx.fillRect(0, 0, width, height);
      ctx.restore();

      // Lorenz attractor ODE solver (precompute points)
      function getLorenzPoints(numPoints = 2000, dt = 0.005, sigma = 10, rho = 28, beta = 8 / 3) {
        let x = 0.1, y = 1, z = 1.05;
        const points = [];
        for (let i = 0; i < numPoints; i++) {
          const dx = sigma * (y - x);
          const dy = x * (rho - z) - y;
          const dz = x * y - beta * z;
          x += dx * dt;
          y += dy * dt;
          z += dz * dt;
          points.push({ x, y, z });
        }
        return points;
      }
      const points = getLorenzPoints(2000);
      const total = points.length;
      const tailLength = 120;
      
      // Project 3D to 2D
      function project({ x, y, z }: { x: number; y: number; z: number }) {
        const angle = Math.PI / 6;
        const scale = Math.min(width, height) * 0.18;
        const x2d = x * Math.cos(angle) - z * Math.sin(angle);
        const y2d = y;
        return [width / 2 + x2d * scale, height / 2 + y2d * scale];
      }
      
      // Draw faded full curve
      ctx.save();
      ctx.globalAlpha = 0.18;
      ctx.beginPath();
      for (let i = 0; i < total; i++) {
        const [x, y] = project(points[i]);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = "#60a5fa";
      ctx.lineWidth = 2.5;
      ctx.shadowColor = "#2563eb";
      ctx.shadowBlur = 16;
      ctx.stroke();
      ctx.restore();
      
      // Update head position with continuous motion
      // Randomly change velocity occasionally
      if (Math.random() < 0.02) {
        velocityRef.current = (Math.random() * 3 + 0.5) * (Math.random() < 0.5 ? 1 : -1);
      }
      
      // Update position with current velocity
      headPositionRef.current += velocityRef.current;
      
      // Wrap around the points array for infinite movement
      // Using modulo to keep within bounds, but handling negative positions too
      headPositionRef.current = ((headPositionRef.current % total) + total) % total;
      
      // Animate the tail
      ctx.save();
      ctx.beginPath();
      for (let i = 0; i < tailLength; i++) {
        // Calculate index with wrap-around
        const idx = Math.floor((headPositionRef.current + i) % total);
        const [x, y] = project(points[idx]);
        
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = "#fbbf24";
      ctx.lineWidth = 5;
      ctx.shadowColor = "#fbbf24";
      ctx.shadowBlur = 32;
      ctx.globalAlpha = 0.85;
      ctx.stroke();
      ctx.restore();
      
      // Glowing head dot
      const headIdx = Math.floor((headPositionRef.current + tailLength - 1) % total);
      let [hx, hy] = project(points[headIdx]);
      const jitter = 2;
      hx += (Math.random() - 0.5) * jitter;
      hy += (Math.random() - 0.5) * jitter;
      ctx.save();
      ctx.beginPath();
      ctx.arc(hx, hy, 8, 0, 2 * Math.PI);
      ctx.fillStyle = "#fbbf24";
      ctx.shadowColor = "#fbbf24";
      ctx.shadowBlur = 24;
      ctx.globalAlpha = 0.7;
      ctx.fill();
      ctx.restore();
    }

    function animate(time: number) {
      if (variant === "paraboloid") drawParaboloid(time);
      else if (variant === "lorenz") drawLorenz(time);
      animationFrameId = requestAnimationFrame(animate);
    }
    animate(performance.now());
    window.addEventListener("resize", resize);
    return () => {
      window.removeEventListener("resize", resize);
      cancelAnimationFrame(animationFrameId);
    };
  }, [variant]);

  return (
    <canvas
      ref={canvasRef}
      style={{
        width: "100%",
        height: "100%",
        display: "block",
        position: "absolute",
        inset: 0,
        zIndex: 0,
        pointerEvents: "none",
        borderRadius: "inherit",
      }}
      aria-hidden="true"
    />
  );
}