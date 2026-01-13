"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { GlassCard } from "@/components/ui/glass-card";

gsap.registerPlugin(ScrollTrigger);

export function CTAFinal() {
  const container = useRef(null);

  useGSAP(() => {
    gsap.from(".cta-content", {
      scrollTrigger: {
        trigger: container.current,
        start: "top 80%",
      },
      scale: 0.9,
      opacity: 0,
      duration: 0.8,
      ease: "power3.out"
    });
  }, { scope: container });

  return (
    <section ref={container} className="py-24 container relative">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent to-cyan-900/10 pointer-events-none" />
      
      <GlassCard className="cta-content relative overflow-hidden text-center py-20 px-6 border-cyan-500/30">
        {/* Animated Background Mesh inside card */}
        <div className="absolute inset-0 opacity-30">
            <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/40 rounded-full blur-[100px] animate-pulse" />
            <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/40 rounded-full blur-[100px] animate-pulse delay-1000" />
        </div>

        <div className="relative z-10 max-w-3xl mx-auto space-y-8">
            <h2 className="text-4xl md:text-5xl font-bold tracking-tight">
                Ready to Find Your <br />
                <span className="text-cyan-400">Perfect AI Stack?</span>
            </h2>
            
            <p className="text-xl text-blue-100/70">
                Join thousands of AI engineers using ToolChainDev to discovering the best tools for their next breakthrough.
            </p>
            
            <div className="flex flex-col sm:flex-row justify-center gap-4 pt-4">
                 <Link 
                    href="/tools" 
                    className="group relative px-8 py-4 rounded-full bg-cyan-500 hover:bg-cyan-400 text-white font-bold text-lg transition-all hover:shadow-[0_0_40px_rgba(14,165,233,0.6)] hover:-translate-y-1"
                >
                    <span className="flex items-center gap-2">
                    Start Browsing
                    <ArrowRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
                    </span>
                </Link>
            </div>
        </div>
      </GlassCard>
    </section>
  );
}
