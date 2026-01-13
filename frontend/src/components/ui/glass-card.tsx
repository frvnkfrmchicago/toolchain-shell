"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";

export function GlassCard({ 
  children, 
  className = "",
  hoverEffect = true
}: { 
  children: React.ReactNode; 
  className?: string;
  hoverEffect?: boolean;
}) {
  const cardRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    if (!hoverEffect || !cardRef.current) return;

    const card = cardRef.current;
    
    // Mouse move effect for tilt/glare could go here if we wanted complex 3D,
    // but we'll stick to the CSS-based hover scale/glow for performance 
    // and use GSAP for entrance if needed later.
    
    // For now, this component is primarily a layout container that applies the 'glass-card' utility
  }, { scope: cardRef });

  return (
    <div 
      ref={cardRef}
      className={`glass-card p-6 ${className}`}
    >
      {children}
    </div>
  );
}
