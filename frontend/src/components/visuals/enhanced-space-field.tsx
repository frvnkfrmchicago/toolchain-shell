"use client";

import { useEffect, useRef } from "react";

export function EnhancedSpaceField() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Set canvas size
    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    // Stars
    const stars: Array<{ x: number; y: number; size: number; opacity: number; twinkleSpeed: number }> = [];
    for (let i = 0; i < 200; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 1.5,
        opacity: Math.random() * 0.7 + 0.3,
        twinkleSpeed: Math.random() * 0.02 + 0.01,
      });
    }

    let frame = 0;

    const animate = () => {
      if (!ctx || !canvas) return;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw stars with twinkling
      stars.forEach((star) => {
        star.opacity += star.twinkleSpeed;
        if (star.opacity > 1 || star.opacity < 0.3) {
          star.twinkleSpeed *= -1;
        }

        ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity})`;
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
        ctx.fill();
      });

      frame++;
      requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener("resize", resize);
    };
  }, []);

  return (
    <>
      {/* Canvas stars */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 pointer-events-none"
      />

      {/* Floating planets */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div
          className="planet absolute top-20 left-10 w-32 h-32 rounded-full bg-gradient-to-br from-neon-cyan/20 to-electric-blue/10 blur-2xl animate-float"
          style={{ filter: "blur(80px)" }}
        />
        <div
          className="planet absolute bottom-40 right-20 w-48 h-48 rounded-full bg-gradient-to-br from-ice-blue/10 to-neon-cyan/5 blur-3xl animate-float-delayed"
          style={{ filter: "blur(100px)" }}
        />
        <div
          className="planet absolute top-1/2 left-1/3 w-24 h-24 rounded-full bg-gradient-to-br from-electric-blue/15 to-neon-cyan/10 blur-2xl animate-float"
          style={{ filter: "blur(60px)", animationDelay: "5s" }}
        />
      </div>

      {/* Nebula glow effects */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-neon-cyan/5 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-electric-blue/5 blur-[120px] rounded-full pointer-events-none" />
    </>
  );
}
