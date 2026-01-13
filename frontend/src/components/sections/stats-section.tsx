"use client";

import { useRef, useState, useEffect } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Zap, Database, Code2, Network, Eye, Cloud, Shield, Share2 } from "lucide-react";

gsap.registerPlugin(ScrollTrigger);

const stats = [
  { value: 90, suffix: "+", label: "Tools Indexed", icon: Zap },
  { value: 8, suffix: "", label: "Categories", icon: Database },
  { value: 24, suffix: "+", label: "MCP Servers", icon: Network },
  { value: 15, suffix: "+", label: "Frameworks", icon: Code2 },
];

const categories = [
  { name: "MCP Servers", count: 24, icon: Network, color: "bg-amber-500" },
  { name: "AI Models", count: 18, icon: Zap, color: "bg-violet-500" },
  { name: "Vector DBs", count: 12, icon: Database, color: "bg-amber-500" },
  { name: "Frameworks", count: 15, icon: Code2, color: "bg-violet-500" },
  { name: "Observability", count: 8, icon: Eye, color: "bg-amber-500" },
  { name: "Deployment", count: 10, icon: Cloud, color: "bg-violet-500" },
  { name: "Security", count: 6, icon: Shield, color: "bg-amber-500" },
  { name: "Agents", count: 9, icon: Share2, color: "bg-violet-500" },
];

function AnimatedCounter({ value, suffix }: { value: number; suffix: string }) {
  const [count, setCount] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          let start = 0;
          const end = value;
          const duration = 2000;
          const increment = end / (duration / 16);
          
          const timer = setInterval(() => {
            start += increment;
            if (start >= end) {
              setCount(end);
              clearInterval(timer);
            } else {
              setCount(Math.floor(start));
            }
          }, 16);
          
          observer.disconnect();
        }
      },
      { threshold: 0.5 }
    );
    
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [value]);

  return <span ref={ref}>{count}{suffix}</span>;
}

export function StatsSection() {
  const container = useRef(null);

  useGSAP(() => {
    gsap.from(".stat-card", {
      scrollTrigger: {
        trigger: container.current,
        start: "top 80%",
        toggleActions: "play none none reverse",
      },
      y: 40,
      opacity: 0,
      duration: 0.6,
      stagger: 0.1,
      ease: "power3.out",
    });

    gsap.from(".category-bar", {
      scrollTrigger: {
        trigger: ".categories-section",
        start: "top 85%",
        toggleActions: "play none none reverse",
      },
      scaleX: 0,
      transformOrigin: "left",
      duration: 0.8,
      stagger: 0.08,
      ease: "power3.out",
    });
  }, { scope: container });

  return (
    <section ref={container} className="py-24">
      <div className="container px-6 max-w-5xl mx-auto">
        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-20">
          {stats.map((stat, idx) => (
            <div 
              key={idx}
              className="stat-card text-center p-6 rounded-2xl bg-white/5 border border-white/10 hover:border-amber-500/30 transition-colors"
            >
              <div className="flex justify-center mb-3">
                <stat.icon className="w-6 h-6 text-amber-400" />
              </div>
              <div className="text-4xl md:text-5xl font-bold text-white mb-2 font-heading">
                <AnimatedCounter value={stat.value} suffix={stat.suffix} />
              </div>
              <div className="text-sm text-white/50 uppercase tracking-wider">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Category Breakdown */}
        <div className="categories-section">
          <h3 className="text-xl font-semibold text-white mb-8 text-center">
            Categories <span className="text-white/50 font-normal">at a glance</span>
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {categories.map((cat, idx) => (
              <div key={idx} className="flex items-center gap-4">
                <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center shrink-0">
                  <cat.icon className="w-4 h-4 text-white/50" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-white/70">{cat.name}</span>
                    <span className="text-xs text-white/40 font-mono">{cat.count}</span>
                  </div>
                  <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                    <div 
                      className={`category-bar h-full ${cat.color} rounded-full`}
                      style={{ width: `${(cat.count / 24) * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
