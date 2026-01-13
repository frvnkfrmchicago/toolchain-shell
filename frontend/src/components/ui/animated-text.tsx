"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";

export function AnimatedText({ 
  text, 
  className = "", 
  delay = 0,
  tag = "div" 
}: { 
  text: string; 
  className?: string; 
  delay?: number;
  tag?: "h1" | "h2" | "h3" | "h4" | "p" | "span" | "div";
}) {
  const container = useRef<HTMLElement>(null);
  const Tag = tag as any; // Cast tag to any to allow dynamic component usage with ref

  useGSAP(() => {
    if (!container.current) return;
    const words = container.current.querySelectorAll(".word");
    gsap.from(words, {
      y: 20,
      opacity: 0,
      duration: 0.8,
      stagger: 0.05,
      delay: delay,
      ease: "power3.out",
    });
  }, { scope: container });

  return (
    <Tag ref={container} className={`overflow-hidden ${className}`}>
      <span className="sr-only">{text}</span>
      {text.split(" ").map((word, i) => (
        <span key={i} className="word inline-block mr-[0.25em] will-change-transform">
          {word}
        </span>
      ))}
    </Tag>
  );
}
