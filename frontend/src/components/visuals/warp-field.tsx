"use client";

import { useRef, useEffect } from "react";

export function WarpField() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let width = window.innerWidth;
    let height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;

    const stars: { x: number; y: number; z: number; color: string }[] = [];
    const STAR_COUNT = 800;
    const SPEED = 2; // Base speed
    
    // Initialize stars
    for (let i = 0; i < STAR_COUNT; i++) {
        stars.push({
            x: (Math.random() - 0.5) * width * 2,
            y: (Math.random() - 0.5) * height * 2,
            z: Math.random() * width,
            color: Math.random() > 0.8 ? "#00F0FF" : "#FFFFFF" // 20% Cyan, 80% White
        });
    }

    const animate = () => {
      // Clear with trail effect (optional, strictly clearing for now for sharpness)
      ctx.fillStyle = "#030305"; // Void background
      ctx.fillRect(0, 0, width, height);

      // Center
      const cx = width / 2;
      const cy = height / 2;

      stars.forEach((star) => {
        // Z-movement
        star.z -= SPEED;

        // Reset if behind camera
        if (star.z <= 0) {
            star.z = width;
            star.x = (Math.random() - 0.5) * width * 2;
            star.y = (Math.random() - 0.5) * height * 2;
        }

        // Projection
        const x = (star.x / star.z) * 100 + cx;
        const y = (star.y / star.z) * 100 + cy;
        
        // Scale by distance (closer = bigger)
        const size = (1 - star.z / width) * 2;
        const opacity = (1 - star.z / width);

        if (x > 0 && x < width && y > 0 && y < height) {
            ctx.fillStyle = star.color;
            ctx.globalAlpha = opacity;
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fill();
            ctx.globalAlpha = 1.0;
        }
      });

      requestAnimationFrame(animate);
    };

    const handleResize = () => {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
    };

    window.addEventListener("resize", handleResize);
    const animationId = requestAnimationFrame(animate);

    return () => {
        window.removeEventListener("resize", handleResize);
        cancelAnimationFrame(animationId);
    };
  }, []);

  return (
    <canvas 
        ref={canvasRef} 
        className="fixed inset-0 z-[-1] pointer-events-none"
    />
  );
}
