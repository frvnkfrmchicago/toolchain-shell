"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";
import { GlassCard } from "@/components/ui/glass-card";
import { Search, Zap, RefreshCw } from "lucide-react";

gsap.registerPlugin(ScrollTrigger);

export function FeaturesBento() {
  const container = useRef(null);

  useGSAP(() => {
    gsap.from(".bento-card", {
      scrollTrigger: {
        trigger: container.current,
        start: "top 75%",
      },
      scale: 0.9,
      opacity: 0,
      duration: 0.8,
      stagger: 0.2, // Stagger effect
      ease: "back.out(1.7)" // Bouncy entrance
    });
  }, { scope: container });

  return (
    <section ref={container} className="py-24 container relative">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 grid-rows-2 h-auto md:h-[600px]">
        
        {/* Large Card 1: Semantic Search */}
        <div className="bento-card md:col-span-2 row-span-1 md:row-span-2 h-full">
          <GlassCard className="h-full flex flex-col justify-between overflow-hidden relative group">
            <div className="relative z-10">
              <div className="w-12 h-12 rounded-full bg-cyan-500/20 flex items-center justify-center mb-6">
                <Search className="w-6 h-6 text-cyan-400" />
              </div>
              <h3 className="text-2xl font-bold mb-2">Semantic Search</h3>
              <p className="text-blue-100/60 max-w-sm">
                Don&apos;t guess keywords. Ask in natural language like &quot;Best vector DB for Python&quot; and get precise, intelligent recommendations.
              </p>
            </div>
            
            {/* Visual: Search UI Mockup */}
            <div className="mt-8 bg-black/40 border border-white/10 rounded-t-xl p-4 transform translate-y-4 group-hover:translate-y-2 transition-transform duration-500">
              <div className="flex gap-2 mb-4">
                <div className="w-3 h-3 rounded-full bg-red-500/50" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
                <div className="w-3 h-3 rounded-full bg-green-500/50" />
              </div>
              <div className="h-8 bg-white/10 rounded w-3/4 mb-4 animate-pulse" />
              <div className="space-y-2">
                <div className="h-16 bg-white/5 rounded w-full" />
                <div className="h-16 bg-white/5 rounded w-full" />
              </div>
            </div>
          </GlassCard>
        </div>

        {/* Small Card 2: AI Powered */}
        <div className="bento-card col-span-1 row-span-1">
          <GlassCard className="h-full flex flex-col justify-center items-center text-center group">
            <div className="w-16 h-16 rounded-full bg-purple-500/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <Zap className="w-8 h-8 text-purple-400" />
            </div>
            <h3 className="font-bold text-lg mb-1">AI-Powered</h3>
            <p className="text-sm text-blue-100/60">
              Powered by advanced LLMs to understand your technical constraints.
            </p>
          </GlassCard>
        </div>

        {/* Small Card 3: Always Updated */}
        <div className="bento-card col-span-1 row-span-1">
          <GlassCard className="h-full flex flex-col justify-center items-center text-center group">
             <div className="w-16 h-16 rounded-full bg-orange-500/20 flex items-center justify-center mb-4 group-hover:rotate-180 transition-transform duration-700">
              <RefreshCw className="w-8 h-8 text-orange-400" />
            </div>
            <h3 className="font-bold text-lg mb-1">Live Updates</h3>
            <p className="text-sm text-blue-100/60">
              Our index triggers daily lookups to ensure versions and docs are fresh.
            </p>
          </GlassCard>
        </div>
      </div>
    </section>
  );
}
