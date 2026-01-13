"use client";

import { useRef, useState } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { Terminal, Hexagon, Send, Layers, ArrowRight } from "lucide-react";
import { AuroraMesh } from "@/components/visuals/aurora-mesh";
import { SearchModal } from "@/components/search-modal";
import { useSearchModal } from "@/hooks/use-search-modal";
import Link from "next/link";
import { useRouter } from "next/navigation";

export function Hero() {
  const container = useRef(null);
  const [inputValue, setInputValue] = useState("");
  const { isOpen, openModal, closeModal } = useSearchModal();
  const router = useRouter();

  useGSAP(() => {
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    // Entrance
    tl.from(".hero-content", {
      y: 30,
      opacity: 0,
      duration: 1,
      delay: 0.2
    })
    .from(".hero-input-section", {
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
    .from(".context-card", {
      y: 20,
      opacity: 0,
      duration: 0.6,
      stagger: 0.1
    }, "-=0.3");

  }, { scope: container });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      // Navigate to /ask with query
      router.push(`/ask?q=${encodeURIComponent(inputValue.trim())}`);
    }
  };

  const handleOpenModal = () => {
    openModal(inputValue);
  };

  return (
    <>
      <section ref={container} className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
        <AuroraMesh />

        <div className="container relative z-10 px-6 text-center hero-content max-w-5xl">
          {/* Headline with proper hierarchy - NEW COLORS */}
          <h1 className="text-5xl md:text-7xl lg:text-[5.5rem] font-bold tracking-tight mb-6 leading-[1.05] font-heading">
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-amber-500 to-orange-500 mb-3">
              ToolChainDev
            </span>
            <span className="block text-white text-4xl md:text-5xl lg:text-6xl font-medium">
              The AI Development Stack Index
            </span>
          </h1>

          {/* Value prop - proper spacing and hierarchy */}
          <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto mb-10 leading-relaxed font-light">
            MCP servers, AI models, vector databases, frameworks, observability tools, and deployment platforms—all indexed, searchable, and explained by AI.
          </p>

          {/* AI Input Section - NEW COLORS */}
          <div className="hero-input-section max-w-2xl mx-auto mb-12">
            <form onSubmit={handleSubmit} className="relative group">
              <div className="absolute -inset-1 bg-gradient-to-r from-amber-500 via-purple-600 to-violet-600 rounded-xl opacity-30 group-hover:opacity-50 blur-lg transition-opacity duration-500" />
              <div className="relative flex items-center bg-[#0A0A12] border border-white/10 rounded-xl overflow-hidden group-hover:border-amber-500/30 transition-colors">
                <div className="pl-5 pr-3">
                  <Hexagon className="w-5 h-5 text-amber-500/60" />
                </div>
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Ask anything about AI tools, MCP servers, frameworks..."
                  className="flex-1 py-5 px-2 bg-transparent text-white placeholder:text-white/40 outline-none text-lg"
                />
                <button
                  type="submit"
                  className="m-2 px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 text-void-bg rounded-lg font-semibold hover:shadow-lg hover:shadow-amber-500/30 transition-all flex items-center gap-2 group/btn"
                >
                  <span className="hidden sm:inline">Consult</span>
                  <Send className="w-4 h-4 group-hover/btn:translate-x-0.5 transition-transform" />
                </button>
              </div>
            </form>
            
            {/* Quick suggestions */}
            <div className="flex flex-wrap justify-center gap-2 mt-4">
              {["Best MCP for PostgreSQL?", "Compare vector DBs", "LLM observability tools"].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => setInputValue(suggestion)}
                  className="px-3 py-1.5 text-xs text-white/50 bg-white/5 border border-white/10 rounded-full hover:bg-amber-500/10 hover:text-amber-400/70 hover:border-amber-500/20 transition-all"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>

          {/* Secondary CTAs */}
          <div className="flex flex-wrap items-center justify-center gap-4 mb-20">
            <Link href="/tools" className="hero-cta">
              <button className="group px-8 py-4 bg-white/5 border border-white/10 text-white rounded-lg font-medium hover:bg-amber-500/10 hover:border-amber-500/20 transition-all flex items-center gap-2">
                <Layers className="w-4 h-4 text-amber-500" />
                Browse the Index
                <ArrowRight className="w-4 h-4 opacity-50 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
              </button>
            </Link>

            <button
              onClick={handleOpenModal}
              className="hero-cta text-white/60 hover:text-white transition-colors text-sm font-medium group"
            >
              <span className="flex items-center gap-2">
                Quick search
                <kbd className="px-2 py-1 text-xs bg-white/10 border border-white/20 rounded font-mono group-hover:border-amber-500/40 transition-colors">⌘K</kbd>
              </span>
            </button>
          </div>

          {/* Stats - social proof with proper spacing - NEW COLORS */}
          <div className="grid grid-cols-3 gap-8 md:gap-16 max-w-2xl mx-auto pt-8 border-t border-white/10">
            <div className="context-card">
              <div className="text-3xl md:text-4xl font-bold text-amber-400 mb-1">90+</div>
              <div className="text-sm text-white/50">Tools Indexed</div>
            </div>
            <div className="context-card">
              <div className="text-3xl md:text-4xl font-bold text-violet-400 mb-1">8</div>
              <div className="text-sm text-white/50">Categories</div>
            </div>
            <div className="context-card">
              <div className="text-3xl md:text-4xl font-bold text-amber-400 mb-1">AI</div>
              <div className="text-sm text-white/50">Powered Search</div>
            </div>
          </div>
        </div>
      </section>

      {/* Search Modal */}
      <SearchModal
        isOpen={isOpen}
        onClose={closeModal}
        initialQuery={inputValue}
      />
    </>
  );
}
