"use client";

import { useRef, useState, useEffect, useCallback } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Cpu, Terminal, ArrowRight, CornerDownLeft, Hexagon, Zap, Layers } from "lucide-react";
import Link from "next/link";

gsap.registerPlugin(ScrollTrigger);

// Multiple terminal messages with variety
const terminalMessages = [
  {
    query: "Find me an MCP server for PostgreSQL with read/write capabilities...",
    response: {
      title: "Analysis Complete",
      results: [
        { name: "@supabase/mcp-server", tag: "Official" },
        { name: "pg-vector-mcp", tag: "Community" },
        { name: "neon-db-mcp", tag: "Trending" },
      ]
    }
  },
  {
    query: "Compare vector databases for RAG applications with 1M+ embeddings",
    response: {
      title: "Comparison Ready",
      results: [
        { name: "Pinecone", tag: "Fastest" },
        { name: "Weaviate", tag: "Open Source" },
        { name: "Qdrant", tag: "Cost-Effective" },
      ]
    }
  },
  {
    query: "Best observability tools for LLM applications in production?",
    response: {
      title: "Stack Recommended",
      results: [
        { name: "LangSmith", tag: "LangChain" },
        { name: "Weights & Biases", tag: "Popular" },
        { name: "Helicone", tag: "Lightweight" },
      ]
    }
  },
  {
    query: "Show me agent frameworks with multi-agent support and tool calling",
    response: {
      title: "Frameworks Found",
      results: [
        { name: "CrewAI", tag: "Hot 🔥" },
        { name: "AutoGen", tag: "Microsoft" },
        { name: "LangGraph", tag: "Flexible" },
      ]
    }
  }
];

export function AskDemo() {
  const container = useRef(null);
  const [typedText, setTypedText] = useState("");
  const [messageIndex, setMessageIndex] = useState(0);
  const [showResponse, setShowResponse] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const typingRef = useRef<NodeJS.Timeout | null>(null);

  const currentMessage = terminalMessages[messageIndex];

  const startTyping = useCallback(() => {
    // Reset state
    setTypedText("");
    setShowResponse(false);
    setIsTyping(true);
    
    let i = 0;
    const fullText = currentMessage.query;
    
    // Clear any existing interval
    if (typingRef.current) {
      clearInterval(typingRef.current);
    }
    
    typingRef.current = setInterval(() => {
      if (i <= fullText.length) {
        setTypedText(fullText.slice(0, i));
        i++;
      } else {
        if (typingRef.current) clearInterval(typingRef.current);
        setIsTyping(false);
        // Show response after a brief pause
        setTimeout(() => setShowResponse(true), 300);
        // Move to next message after delay
        setTimeout(() => {
          setMessageIndex(prev => (prev + 1) % terminalMessages.length);
        }, 4000);
      }
    }, 25); // Fast typing speed!
  }, [currentMessage.query]);

  // Restart typing when message index changes
  useEffect(() => {
    if (!isTyping && typedText === "") {
      startTyping();
    }
  }, [messageIndex, isTyping, typedText, startTyping]);

  useGSAP(() => {
    // Reveal animation
    gsap.from(".terminal-window", {
      scrollTrigger: {
        trigger: container.current,
        start: "top 70%",
      },
      scale: 0.95,
      opacity: 0,
      duration: 1,
      ease: "power4.out"
    });

    // Scroll-triggered restart
    ScrollTrigger.create({
      trigger: container.current,
      start: "top 60%",
      onEnter: () => {
        setMessageIndex(0);
        startTyping();
      },
      onEnterBack: () => {
        // Re-trigger when scrolling back up too!
        setMessageIndex(prev => (prev + 1) % terminalMessages.length);
        startTyping();
      }
    });

  }, { scope: container });

  // Cleanup
  useEffect(() => {
    return () => {
      if (typingRef.current) clearInterval(typingRef.current);
    };
  }, []);

  return (
    <section ref={container} className="relative py-24 overflow-hidden">
      {/* Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-violet-900/5 to-amber-900/5 pointer-events-none" />

      <div className="container px-4 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          
          {/* Left: Content */}
          <div>
            <h2 className="text-4xl md:text-5xl font-bold tracking-tight text-white mb-6 leading-tight font-heading">
              Consult About<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-violet-400">Any Tool or Stack</span>
            </h2>

            <p className="text-lg text-white/60 mb-10 font-light max-w-lg leading-relaxed">
              Our AI assistant knows the entire ToolChainDev index. Get personalized recommendations, compare tools, and understand which stack fits your project.
            </p>

            {/* Two ways to use it */}
            <div className="space-y-4 mb-10 max-w-lg">
              <div className="flex items-start gap-4 p-4 bg-void-card/40 border border-white/10 rounded hover:border-amber-500/30 transition-colors group">
                <div className="p-2 bg-amber-500/10 rounded shrink-0 group-hover:bg-amber-500/20 transition-colors">
                  <Terminal className="w-5 h-5 text-amber-400" />
                </div>
                <div>
                  <h3 className="text-white font-semibold mb-1">Quick Search (⌘K)</h3>
                  <p className="text-sm text-white/50">Instant modal for fast questions</p>
                </div>
              </div>

              <div className="flex items-start gap-4 p-4 bg-void-card/40 border border-white/10 rounded hover:border-violet-500/30 transition-colors group">
                <div className="p-2 bg-violet-500/10 rounded shrink-0 group-hover:bg-violet-500/20 transition-colors">
                  <Layers className="w-5 h-5 text-violet-400" />
                </div>
                <div>
                  <h3 className="text-white font-semibold mb-1">Full Consultation (/ask)</h3>
                  <p className="text-sm text-white/50">Dedicated page for deep conversations</p>
                </div>
              </div>
            </div>

            <Link href="/ask">
              <button className="group inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-amber-500 to-orange-500 text-void-bg rounded font-semibold hover:shadow-xl hover:shadow-amber-500/30 transition-all hover:scale-[1.02]">
                <span>Start Consultation</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
            </Link>
          </div>

          {/* Right: Terminal Visual */}
          <div className="terminal-window relative">
            {/* Terminal Chrome */}
            <div className="w-full bg-[#1A1A24] rounded-t-lg p-3 flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500/70 hover:bg-red-500 transition-colors" />
              <div className="w-3 h-3 rounded-full bg-yellow-500/70 hover:bg-yellow-500 transition-colors" />
              <div className="w-3 h-3 rounded-full bg-green-500/70 hover:bg-green-500 transition-colors" />
              <div className="ml-auto flex items-center gap-2 text-xs text-white/30 font-mono">
                <Zap className="w-3 h-3 text-amber-400 animate-pulse" />
                <span>toolchain-ai — live</span>
              </div>
            </div>

            {/* Terminal Body */}
            <div className="bg-black/90 backdrop-blur-xl border border-white/5 border-t-0 rounded-b-lg p-6 font-mono text-sm h-[420px] flex flex-col shadow-2xl relative overflow-hidden">
                {/* Subtle grid pattern */}
                <div className="absolute inset-0 opacity-5" style={{
                  backgroundImage: 'linear-gradient(to right, #F59E0B 1px, transparent 1px), linear-gradient(to bottom, #F59E0B 1px, transparent 1px)',
                  backgroundSize: '20px 20px'
                }} />

                {/* Chat History */}
                <div className="flex-1 space-y-6 relative z-10">
                    {/* System Msg */}
                    <div className="text-white/40">
                        <span className="text-amber-400">➜</span> system init... <span className="text-amber-400">Done.</span>
                        <span className="ml-2 text-xs text-green-400/60">[{terminalMessages.length} queries loaded]</span>
                    </div>

                    {/* User Input (Animated) */}
                    <div className="text-white">
                        <span className="text-amber-400">user@toolchain:~$</span>{" "}
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-white via-amber-300 to-white">{typedText}</span>
                        {isTyping && <span className="animate-pulse inline-block w-2 h-4 bg-amber-400 ml-1 align-middle" />}
                    </div>

                    {/* AI Response */}
                    {showResponse && (
                        <div className="p-4 border-l-2 border-violet-500 bg-gradient-to-r from-violet-500/10 to-transparent text-violet-200 animate-in fade-in slide-in-from-bottom-2 duration-500">
                            <div className="flex items-center gap-2 mb-3 text-violet-400 text-xs uppercase tracking-wider">
                                <Cpu className="w-3 h-3" /> {currentMessage.response.title}
                            </div>
                            <div className="space-y-2">
                              {currentMessage.response.results.map((result, idx) => (
                                <div key={idx} className="flex items-center gap-2">
                                  <span className="text-white/40 text-xs">{idx + 1}.</span>
                                  <span className="text-white font-bold">{result.name}</span>
                                  <span className="text-xs px-2 py-0.5 rounded bg-amber-500/20 text-amber-400">
                                    {result.tag}
                                  </span>
                                </div>
                              ))}
                            </div>
                        </div>
                    )}
                </div>

                {/* Input Bar */}
                <div className="mt-auto pt-4 border-t border-white/10 flex items-center gap-2 text-white/50 relative z-10">
                    <Terminal className="w-4 h-4 text-amber-400/50" />
                    <span className="flex-1">
                      {isTyping ? (
                        <span className="text-amber-400/70">Processing query...</span>
                      ) : showResponse ? (
                        <span className="text-green-400/70">Ready for next query</span>
                      ) : (
                        <span>Awaiting command...</span>
                      )}
                    </span>
                    <CornerDownLeft className="w-4 h-4 opacity-50" />
                </div>
            </div>

            {/* Glow Decorations */}
            <div className="absolute -bottom-10 -right-10 w-40 h-40 bg-amber-500/20 blur-[100px] rounded-full pointer-events-none" />
            <div className="absolute -top-5 -left-5 w-24 h-24 bg-violet-500/20 blur-[80px] rounded-full pointer-events-none" />
          </div>

        </div>
      </div>
    </section>
  );
}
