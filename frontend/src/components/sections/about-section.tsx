"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Lightbulb, ArrowRight } from "lucide-react";
import Link from "next/link";

gsap.registerPlugin(ScrollTrigger);

export function AboutSection() {
  const container = useRef(null);

  useGSAP(() => {
    gsap.from(".about-content", {
      scrollTrigger: {
        trigger: container.current,
        start: "top 75%",
        toggleActions: "play none none reverse",
      },
      y: 50,
      opacity: 0,
      duration: 0.8,
      ease: "power3.out",
    });
  }, { scope: container });

  return (
    <section ref={container} className="py-24 relative">
      {/* Subtle divider */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-px bg-gradient-to-r from-transparent via-amber-500/50 to-transparent" />

      <div className="container px-6 max-w-4xl mx-auto">
        <div className="about-content">
          {/* Badge */}
          <div className="flex justify-center mb-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20">
              <Lightbulb className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-400 font-medium">What is ToolChainDev?</span>
            </div>
          </div>

          {/* Main Content */}
          <h2 className="text-3xl md:text-4xl font-bold text-center text-white mb-8 font-heading leading-tight">
            The AI Developer's <span className="text-amber-400">Reference Index</span>
          </h2>

          <div className="space-y-6 text-center">
            <p className="text-lg text-white/70 leading-relaxed">
              AI development is moving fast. New tools, protocols, and frameworks emerge every week—<strong className="text-white">MCP servers</strong>, <strong className="text-white">vector databases</strong>, <strong className="text-white">agent frameworks</strong>, <strong className="text-white">observability platforms</strong>. Keeping track of it all is a job in itself.
            </p>

            <p className="text-lg text-white/70 leading-relaxed">
              <span className="text-amber-400 font-semibold">ToolChainDev indexes everything.</span> We catalog 90+ tools across 8 categories, with detailed comparisons, code examples, pros/cons, and alternatives. Our AI assistant helps you find exactly what you need.
            </p>

            <p className="text-lg text-white/70 leading-relaxed">
              Whether you're building a RAG pipeline, setting up an MCP server, or choosing between LangChain and CrewAI—ToolChainDev is your starting point.
            </p>
          </div>

          {/* CTA */}
          <div className="flex justify-center mt-10">
            <Link href="/tools">
              <button className="group inline-flex items-center gap-2 text-amber-400 hover:text-amber-300 font-medium transition-colors">
                Start exploring the index
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
