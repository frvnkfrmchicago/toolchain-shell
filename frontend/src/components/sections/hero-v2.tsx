"use client";

import { useState, useRef } from "react";
import { motion } from "framer-motion";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { Send, Layers, Search, ArrowRight, Database, Network, Code2, Cpu } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export function HeroV2() {
  const container = useRef(null);
  const [inputValue, setInputValue] = useState("");
  const router = useRouter();

  useGSAP(() => {
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    tl.from(".hero-brand", {
      y: 40,
      opacity: 0,
      duration: 1,
    })
    .from(".hero-tagline", {
      y: 30,
      opacity: 0,
      duration: 0.8,
    }, "-=0.6")
    .from(".hero-input", {
      y: 30,
      opacity: 0,
      duration: 0.8,
    }, "-=0.5")
    .from(".hero-cta", {
      y: 20,
      opacity: 0,
      duration: 0.6,
      stagger: 0.1
    }, "-=0.4")
    .from(".hero-stat", {
      y: 20,
      opacity: 0,
      duration: 0.5,
      stagger: 0.1
    }, "-=0.3");

  }, { scope: container });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      router.push(`/ask?q=${encodeURIComponent(inputValue.trim())}`);
    }
  };

  return (
    <section ref={container} className="relative min-h-[90vh] flex items-center justify-center overflow-hidden pt-20">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-amber-500/5 via-transparent to-violet-500/5" />
      <div className="absolute inset-0" style={{
        backgroundImage: 'radial-gradient(circle at 30% 20%, rgba(245, 158, 11, 0.1), transparent 40%), radial-gradient(circle at 70% 80%, rgba(124, 58, 237, 0.08), transparent 40%)'
      }} />

      <div className="container relative z-10 px-6 max-w-5xl mx-auto">
        {/* Brand */}
        <div className="text-center mb-12">
          <h1 className="hero-brand text-5xl md:text-7xl lg:text-8xl font-bold tracking-tight mb-6 font-heading">
            <span className="text-transparent bg-clip-text" style={{
              background: 'linear-gradient(135deg, #F59E0B 0%, #D97706 50%, #F59E0B 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text'
            }}>
              ToolChainDev
            </span>
          </h1>
          
          <p className="hero-tagline text-xl md:text-2xl text-white/70 max-w-3xl mx-auto leading-relaxed font-light">
            The complete index of <span className="text-amber-400 font-medium">AI development tools</span>—MCP servers, vector databases, agent frameworks, and more. Search, compare, and consult with AI.
          </p>
        </div>

        {/* AI Input Bar */}
        <div className="hero-input max-w-2xl mx-auto mb-10">
          <form onSubmit={handleSubmit} className="relative group">
            {/* Glow Effect */}
            <div className="absolute -inset-1 bg-gradient-to-r from-amber-500/30 via-violet-500/20 to-amber-500/30 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            
            {/* Input Container */}
            <div className="relative flex items-center bg-[#111118] border border-white/10 rounded-2xl overflow-hidden group-focus-within:border-amber-500/40 transition-colors">
              <div className="pl-5 pr-3">
                <Layers className="w-5 h-5 text-amber-500/70" />
              </div>
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask about any AI tool, MCP, framework..."
                className="flex-1 py-5 px-2 bg-transparent text-white placeholder:text-white/40 outline-none text-lg"
              />
              <button
                type="submit"
                className="m-2 px-6 py-3 bg-gradient-to-r from-amber-500 to-amber-600 text-black rounded-xl font-semibold hover:shadow-lg hover:shadow-amber-500/25 transition-all flex items-center gap-2"
              >
                <span className="hidden sm:inline">Consult</span>
                <Send className="w-4 h-4" />
              </button>
            </div>
          </form>
          
          {/* Quick suggestions */}
          <div className="flex flex-wrap justify-center gap-2 mt-4">
            {["What is an MCP?", "Best vector database?", "Compare agent frameworks"].map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => setInputValue(suggestion)}
                className="px-3 py-1.5 text-xs text-white/50 bg-white/5 border border-white/10 rounded-full hover:bg-amber-500/10 hover:text-amber-400 hover:border-amber-500/20 transition-all"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>

        {/* CTAs */}
        <div className="flex flex-wrap items-center justify-center gap-4 mb-16">
          <Link href="/tools" className="hero-cta">
            <button className="group px-8 py-4 bg-white/5 border border-white/10 text-white rounded-xl font-medium hover:bg-amber-500/10 hover:border-amber-500/20 transition-all flex items-center gap-3">
              <Search className="w-4 h-4 text-amber-400" />
              Browse All Tools
              <ArrowRight className="w-4 h-4 opacity-50 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
            </button>
          </Link>
        </div>

        {/* Stats Strip */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto">
          <div className="hero-stat text-center p-4 rounded-xl bg-white/5 border border-white/5">
            <div className="flex justify-center mb-2">
              <Network className="w-5 h-5 text-amber-400" />
            </div>
            <div className="text-2xl md:text-3xl font-bold text-white mb-1">24+</div>
            <div className="text-xs text-white/50 uppercase tracking-wider">MCP Servers</div>
          </div>
          
          <div className="hero-stat text-center p-4 rounded-xl bg-white/5 border border-white/5">
            <div className="flex justify-center mb-2">
              <Database className="w-5 h-5 text-violet-400" />
            </div>
            <div className="text-2xl md:text-3xl font-bold text-white mb-1">12+</div>
            <div className="text-xs text-white/50 uppercase tracking-wider">Vector DBs</div>
          </div>
          
          <div className="hero-stat text-center p-4 rounded-xl bg-white/5 border border-white/5">
            <div className="flex justify-center mb-2">
              <Code2 className="w-5 h-5 text-amber-400" />
            </div>
            <div className="text-2xl md:text-3xl font-bold text-white mb-1">15+</div>
            <div className="text-xs text-white/50 uppercase tracking-wider">Frameworks</div>
          </div>
          
          <div className="hero-stat text-center p-4 rounded-xl bg-white/5 border border-white/5">
            <div className="flex justify-center mb-2">
              <Cpu className="w-5 h-5 text-violet-400" />
            </div>
            <div className="text-2xl md:text-3xl font-bold text-white mb-1">AI</div>
            <div className="text-xs text-white/50 uppercase tracking-wider">Powered</div>
          </div>
        </div>
      </div>
    </section>
  );
}
