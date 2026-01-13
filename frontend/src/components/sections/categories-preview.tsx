"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { VoidCard } from "@/components/ui/void-card";
import { Cpu, Database, Cloud, Network, Code2, Shield, Activity, Share2, Layers, HelpCircle, BookOpen, Zap } from "lucide-react";
import Link from "next/link";
import { cn } from "@/lib/utils";

gsap.registerPlugin(ScrollTrigger);

const categories = [
  { id: "mcp", name: "MCP Servers", count: 24, icon: Network, desc: "Model Context Protocol" },
  { id: "api", name: "AI Models", count: 18, icon: Cpu, desc: "LLMs & APIs" },
  { id: "sdk", name: "Vector DBs", count: 12, icon: Database, desc: "Embeddings Storage" },
  { id: "framework", name: "Frameworks", count: 15, icon: Code2, desc: "LangChain, CrewAI" },
  { id: "observability", name: "Observability", count: 8, icon: Activity, desc: "Monitoring & Tracing" },
  { id: "deployment", name: "Deployment", count: 10, icon: Cloud, desc: "Infrastructure" },
];

const explainers = [
  {
    title: "What is an MCP?",
    subtitle: "Model Context Protocol",
    description: "MCPs are standardized interfaces that let AI models interact with external data sources, APIs, and tools in a secure, structured way.",
    icon: Network,
    color: "from-amber-500/20 to-amber-500/5",
    borderColor: "border-amber-500/30",
    iconColor: "text-amber-400"
  },
  {
    title: "Vector Databases",
    subtitle: "Semantic Search",
    description: "Store and query embeddings for RAG applications. Find semantically similar content at massive scale.",
    icon: Database,
    color: "from-violet-500/20 to-violet-500/5",
    borderColor: "border-violet-500/30",
    iconColor: "text-violet-400"
  },
  {
    title: "Agent Frameworks",
    subtitle: "Autonomous AI",
    description: "Build multi-step AI agents that can reason, plan, and execute complex tasks with tool-calling capabilities.",
    icon: Share2,
    color: "from-orange-500/20 to-orange-500/5",
    borderColor: "border-orange-500/30",
    iconColor: "text-orange-400"
  }
];

export function CategoriesPreview() {
  const container = useRef(null);

  useGSAP(() => {
    // Staggered entrance for cards
    gsap.from(".category-card", {
      scrollTrigger: {
        trigger: container.current,
        start: "top 80%",
        toggleActions: "play none none reverse",
      },
      y: 50,
      opacity: 0,
      duration: 0.6,
      stagger: 0.08,
      ease: "power2.out",
    });

    // Explainer cards with different timing
    gsap.from(".explainer-card", {
      scrollTrigger: {
        trigger: ".explainers-section",
        start: "top 85%",
        toggleActions: "play none none reverse",
      },
      x: -30,
      opacity: 0,
      duration: 0.7,
      stagger: 0.15,
      ease: "power3.out",
    });
  }, { scope: container });

  return (
    <section ref={container} className="relative py-24 z-10">
      <div className="container px-4">
        {/* Section Header */}
        <div className="mb-12 flex items-end justify-between border-b border-white/10 pb-6">
          <div>
            <h2 className="text-3xl font-bold tracking-tight text-white mb-2 font-heading">
              Explore by <span className="text-amber-400">Category</span>
            </h2>
            <p className="text-white/50 text-sm">Browse AI tools organized by type and use case</p>
          </div>
          <div className="hidden md:block text-right">
            <span className="text-amber-400 font-mono text-xs">90+ Tools Indexed</span>
          </div>
        </div>

        {/* Categories Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-16">
          {categories.map((cat) => (
            <Link key={cat.id} href={`/tools?category=${cat.id}`} className="block group">
              <VoidCard className="category-card h-full min-h-[140px] flex flex-col justify-between hover:bg-[#0F0F1A] group-hover:border-amber-500/30">
                <div className="flex justify-between items-start">
                  <div className="p-2 rounded bg-amber-500/10 border border-amber-500/20 group-hover:scale-110 group-hover:bg-amber-500/20 transition-all">
                    <cat.icon className="w-5 h-5 text-amber-400" />
                  </div>
                  <span className="font-mono text-xs text-white/30 group-hover:text-amber-400 transition-colors">
                    {cat.count}
                  </span>
                </div>

                <div className="mt-auto">
                  <h3 className="text-sm font-medium text-white group-hover:text-amber-400 transition-colors">
                    {cat.name}
                  </h3>
                  <p className="text-xs text-white/40 mt-1">{cat.desc}</p>
                  <div className="h-0.5 w-0 bg-gradient-to-r from-amber-500 to-violet-500 mt-2 group-hover:w-full transition-all duration-500" />
                </div>
              </VoidCard>
            </Link>
          ))}
        </div>

        {/* Educational Explainer Section */}
        <div className="explainers-section">
          <div className="flex items-center gap-3 mb-8">
            <div className="p-2 rounded-lg bg-violet-500/10 border border-violet-500/20">
              <BookOpen className="w-5 h-5 text-violet-400" />
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white">Understanding the Stack</h3>
              <p className="text-sm text-white/40">Quick explainers for key concepts</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {explainers.map((item, idx) => (
              <div 
                key={idx} 
                className={cn(
                  "explainer-card p-6 rounded-xl border bg-gradient-to-br transition-all duration-300 hover:scale-[1.02]",
                  item.color,
                  item.borderColor
                )}
              >
                <div className="flex items-start gap-4 mb-4">
                  <div className={cn("p-3 rounded-lg bg-black/30", item.iconColor)}>
                    <item.icon className="w-6 h-6" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white">{item.title}</h4>
                    <p className="text-xs text-white/50 uppercase tracking-wider">{item.subtitle}</p>
                  </div>
                </div>
                <p className="text-sm text-white/70 leading-relaxed">
                  {item.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
