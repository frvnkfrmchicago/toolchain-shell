"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Network, Terminal, Database, Share2 } from "lucide-react";

gsap.registerPlugin(ScrollTrigger);

const concepts = [
  {
    icon: Network,
    title: "MCP Servers",
    subtitle: "Model Context Protocol",
    description: "Standardized interfaces that let AI models securely connect to databases, APIs, and external tools. Think of them as USB ports for AI—plug in any data source.",
    color: "amber",
    examples: ["PostgreSQL MCP", "GitHub MCP", "Filesystem MCP"]
  },
  {
    icon: Terminal,
    title: "CLI Tools",
    subtitle: "Command Line Interfaces",
    description: "Terminal-based tools for AI development workflows. From code generation to model management, CLIs give you precise control over your AI stack.",
    color: "violet",
    examples: ["Ollama", "LangChain CLI", "Vite"]
  },
  {
    icon: Database,
    title: "Vector Databases",
    subtitle: "Embedding Storage",
    description: "Specialized databases that store and query vector embeddings for RAG applications. Enable semantic search across millions of documents in milliseconds.",
    color: "amber",
    examples: ["Pinecone", "Weaviate", "Qdrant"]
  },
  {
    icon: Share2,
    title: "Agent Frameworks",
    subtitle: "Autonomous AI Systems",
    description: "Frameworks for building AI agents that can reason, plan, and execute multi-step tasks. Enable complex workflows with tool-calling capabilities.",
    color: "violet",
    examples: ["CrewAI", "LangGraph", "AutoGen"]
  }
];

export function ConceptGrid() {
  const container = useRef(null);

  useGSAP(() => {
    gsap.from(".concept-card", {
      scrollTrigger: {
        trigger: container.current,
        start: "top 75%",
        toggleActions: "play none none reverse",
      },
      y: 60,
      opacity: 0,
      duration: 0.7,
      stagger: 0.15,
      ease: "power3.out",
    });
  }, { scope: container });

  return (
    <section ref={container} className="py-24 bg-gradient-to-b from-transparent via-violet-500/3 to-transparent">
      <div className="container px-6 max-w-6xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4 font-heading">
            Key <span className="text-violet-400">Concepts</span> Explained
          </h2>
          <p className="text-white/50 max-w-2xl mx-auto">
            New to the AI development ecosystem? Here's a quick primer on the technologies we index.
          </p>
        </div>

        {/* Concept Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {concepts.map((concept, idx) => (
            <div 
              key={idx}
              className={`concept-card p-6 rounded-2xl border transition-all duration-300 hover:scale-[1.02] ${
                concept.color === "amber" 
                  ? "bg-gradient-to-br from-amber-500/10 to-amber-500/5 border-amber-500/20 hover:border-amber-500/40"
                  : "bg-gradient-to-br from-violet-500/10 to-violet-500/5 border-violet-500/20 hover:border-violet-500/40"
              }`}
            >
              {/* Header */}
              <div className="flex items-start gap-4 mb-4">
                <div className={`p-3 rounded-xl ${
                  concept.color === "amber" 
                    ? "bg-amber-500/20 text-amber-400" 
                    : "bg-violet-500/20 text-violet-400"
                }`}>
                  <concept.icon className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white">{concept.title}</h3>
                  <p className={`text-xs uppercase tracking-wider ${
                    concept.color === "amber" ? "text-amber-400/70" : "text-violet-400/70"
                  }`}>
                    {concept.subtitle}
                  </p>
                </div>
              </div>

              {/* Description */}
              <p className="text-white/70 leading-relaxed mb-4">
                {concept.description}
              </p>

              {/* Examples */}
              <div className="flex flex-wrap gap-2">
                {concept.examples.map((example, i) => (
                  <span 
                    key={i}
                    className={`text-xs px-2.5 py-1 rounded-full ${
                      concept.color === "amber"
                        ? "bg-amber-500/10 text-amber-400/80 border border-amber-500/20"
                        : "bg-violet-500/10 text-violet-400/80 border border-violet-500/20"
                    }`}
                  >
                    {example}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
