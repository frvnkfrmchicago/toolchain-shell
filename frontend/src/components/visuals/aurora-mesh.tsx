"use client";

import { useRef, useEffect, useState } from "react";

export function AuroraMesh() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [scrollProgress, setScrollProgress] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? window.scrollY / docHeight : 0;
      setScrollProgress(progress);
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let width = window.innerWidth;
    let height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;

    let time = 0;

    const gradientColors = [
      { r: 245, g: 158, b: 11 },   // Amber Gold
      { r: 124, g: 58, b: 237 },   // Deep Plum
      { r: 30, g: 27, b: 75 },     // Rich Navy
      { r: 253, g: 230, b: 138 },  // Cream Rose
    ];

    const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

    const animate = () => {
      time += 0.003;

      // Create flowing gradient based on scroll + time
      const scrollInfluence = scrollProgress * 0.5;
      
      // Background base
      ctx.fillStyle = "#0A0A12";
      ctx.fillRect(0, 0, width, height);

      // Draw multiple aurora layers
      for (let layer = 0; layer < 4; layer++) {
        ctx.save();
        
        const layerOffset = layer * 0.25;
        const wavePhase = time + layerOffset + scrollInfluence;
        
        // Create curved gradient path
        ctx.beginPath();
        ctx.moveTo(0, height);
        
        for (let x = 0; x <= width; x += 10) {
          const normalizedX = x / width;
          const wave1 = Math.sin(normalizedX * 3 + wavePhase) * 150;
          const wave2 = Math.sin(normalizedX * 5 + wavePhase * 1.5) * 80;
          const wave3 = Math.cos(normalizedX * 2 + wavePhase * 0.7) * 60;
          
          const baseY = height * (0.3 + layer * 0.15);
          const y = baseY + wave1 + wave2 + wave3;
          
          ctx.lineTo(x, y);
        }
        
        ctx.lineTo(width, height);
        ctx.closePath();

        // Create gradient based on layer and scroll
        const colorIndex = (layer + Math.floor(scrollProgress * 2)) % gradientColors.length;
        const nextColorIndex = (colorIndex + 1) % gradientColors.length;
        const t = (scrollProgress * 2) % 1;
        
        const r = Math.round(lerp(gradientColors[colorIndex].r, gradientColors[nextColorIndex].r, t));
        const g = Math.round(lerp(gradientColors[colorIndex].g, gradientColors[nextColorIndex].g, t));
        const b = Math.round(lerp(gradientColors[colorIndex].b, gradientColors[nextColorIndex].b, t));
        
        const gradient = ctx.createLinearGradient(0, 0, width, height);
        gradient.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${0.08 - layer * 0.015})`);
        gradient.addColorStop(0.5, `rgba(${r}, ${g}, ${b}, ${0.12 - layer * 0.02})`);
        gradient.addColorStop(1, `rgba(${r}, ${g}, ${b}, ${0.04 - layer * 0.01})`);
        
        ctx.fillStyle = gradient;
        ctx.fill();
        ctx.restore();
      }

      // Add noise texture overlay
      const imageData = ctx.getImageData(0, 0, width, height);
      const data = imageData.data;
      for (let i = 0; i < data.length; i += 4) {
        const noise = (Math.random() - 0.5) * 8;
        data[i] = Math.max(0, Math.min(255, data[i] + noise));
        data[i + 1] = Math.max(0, Math.min(255, data[i + 1] + noise));
        data[i + 2] = Math.max(0, Math.min(255, data[i + 2] + noise));
      }
      ctx.putImageData(imageData, 0, 0);

      // Add subtle glow orbs
      const orbCount = 3;
      for (let i = 0; i < orbCount; i++) {
        const orbX = width * (0.2 + i * 0.3) + Math.sin(time + i) * 100;
        const orbY = height * 0.3 + Math.cos(time * 0.7 + i) * 80;
        const orbRadius = 150 + Math.sin(time + i * 2) * 50;
        
        const orbGradient = ctx.createRadialGradient(orbX, orbY, 0, orbX, orbY, orbRadius);
        const orbColor = gradientColors[(i + Math.floor(scrollProgress * 3)) % gradientColors.length];
        orbGradient.addColorStop(0, `rgba(${orbColor.r}, ${orbColor.g}, ${orbColor.b}, 0.15)`);
        orbGradient.addColorStop(0.5, `rgba(${orbColor.r}, ${orbColor.g}, ${orbColor.b}, 0.05)`);
        orbGradient.addColorStop(1, "transparent");
        
        ctx.fillStyle = orbGradient;
        ctx.beginPath();
        ctx.arc(orbX, orbY, orbRadius, 0, Math.PI * 2);
        ctx.fill();
      }

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
  }, [scrollProgress]);

  return (
    <canvas 
      ref={canvasRef} 
      className="fixed inset-0 z-[-1] pointer-events-none"
      style={{ filter: "blur(1px)" }}
    />
  );
}
