"use client"
import React, { useRef, useEffect } from "react";

// Lorenz attractor ODE solver (Euler method for simplicity)
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

export default function AnimatedMathBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Rectangle size (confined to top, but much larger)
    const width = window.innerWidth;
    const height = 650; // Larger height
    let dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    // Lorenz points
    const points = getLorenzPoints(2000);
    const total = points.length;
    const tailLength = 120;

    // Project 3D to 2D (simple rotation)
    function project({ x, y, z }: { x: number; y: number; z: number }) {
      // Rotate for a nice view
      const angle = Math.PI / 6;
      const x2d = x * Math.cos(angle) - z * Math.sin(angle);
      const y2d = y;
      return { x: x2d, y: y2d };
    }

    // Find bounds for scaling
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    for (const p of points) {
      const { x, y } = project(p);
      minX = Math.min(minX, x);
      maxX = Math.max(maxX, x);
      minY = Math.min(minY, y);
      maxY = Math.max(maxY, y);
    }
    // Scale up for larger canvas
    const scale = Math.min(width * 0.95 / (maxX - minX), height * 0.95 / (maxY - minY));
    const offsetX = width / 2 - ((minX + maxX) / 2) * scale;
    const offsetY = height / 2 - ((minY + maxY) / 2) * scale;

    let animationFrameId: number;
    function draw(time: number) {
      if (!ctx) return;
      ctx.clearRect(0, 0, width, height);
      // Subtle dark overlay for contrast
      ctx.save();
      ctx.globalAlpha = 0.7;
      ctx.fillStyle = "#0a1626"; // very dark blue
      ctx.fillRect(0, 0, width, height);
      ctx.restore();

      ctx.save();
      ctx.globalAlpha = 0.18;
      // Draw faded full curve
      ctx.beginPath();
      for (let i = 0; i < total; i++) {
        const { x, y } = project(points[i]);
        if (i === 0) ctx.moveTo(offsetX + x * scale, offsetY + y * scale);
        else ctx.lineTo(offsetX + x * scale, offsetY + y * scale);
      }
      ctx.strokeStyle = "#2563eb"; // blue-700, darker for dark mode
      ctx.lineWidth = 3.5;
      ctx.shadowColor = "#1e40af"; // even darker blue
      ctx.shadowBlur = 24;
      ctx.stroke();
      ctx.restore();

      // Animate the racetrack head (even slower)
      const speed = 0.00015; // much slower
      const head = ((time * speed) % 1) * (total - tailLength);
      ctx.save();
      ctx.beginPath();
      for (let i = 0; i < tailLength; i++) {
        const idx = Math.floor(head + i);
        if (idx >= total) break;
        const { x, y } = project(points[idx]);
        if (i === 0) ctx.moveTo(offsetX + x * scale, offsetY + y * scale);
        else ctx.lineTo(offsetX + x * scale, offsetY + y * scale);
      }
      ctx.strokeStyle = "#60a5fa"; // blue-400
      ctx.lineWidth = 7;
      ctx.shadowColor = "#3b82f6"; // blue-500
      ctx.shadowBlur = 40;
      ctx.globalAlpha = 0.95;
      ctx.stroke();
      ctx.restore();

      // Glowing head dot
      const { x, y } = project(points[Math.floor(head + tailLength - 1)]);
      ctx.save();
      ctx.beginPath();
      ctx.arc(offsetX + x * scale, offsetY + y * scale, 12, 0, 2 * Math.PI);
      ctx.fillStyle = "#60a5fa";
      ctx.shadowColor = "#3b82f6";
      ctx.shadowBlur = 48;
      ctx.globalAlpha = 0.85;
      ctx.fill();
      ctx.restore();

      animationFrameId = requestAnimationFrame(draw);
    }
    animationFrameId = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(animationFrameId);
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100vw",
        height: "650px",
        zIndex: 0,
        pointerEvents: "none",
        opacity: 1,
        filter: "blur(0.5px)",
        background: "transparent",
        display: "block",
      }}
      aria-hidden="true"
    />
  );
} 