"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { ArrowLeft, ExternalLink, Github, Check, X, Copy, Terminal, Layers } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { API_URL, formatCategory, formatPricing, cn } from "@/lib/utils";
import type { AITool } from "@/types";

const pricingColors: Record<string, string> = {
  free: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30",
  freemium: "text-amber-400 bg-amber-500/10 border-amber-500/30",
  paid: "text-violet-400 bg-violet-500/10 border-violet-500/30",
  enterprise: "text-rose-400 bg-rose-500/10 border-rose-500/30",
};

export default function ToolDetailPage() {
  const params = useParams();
  const toolId = Array.isArray(params?.id) ? params.id[0] : params?.id;
  const [tool, setTool] = useState<AITool | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!toolId) {
      setIsLoading(false);
      return;
    }

    const fetchTool = async () => {
      setIsLoading(true);
      try {
        const response = await fetch(`${API_URL}/api/tools/${toolId}`);
        if (response.ok) {
          const data = await response.json();
          setTool(data);
        }
      } catch {
        // Error handled silently
      } finally {
        setIsLoading(false);
      }
    };

    fetchTool();
  }, [toolId]);

  const copyCode = () => {
    if (tool) {
      navigator.clipboard.writeText(tool.code_example);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] text-white">
        <div className="max-w-5xl mx-auto px-6 pt-24">
          <div className="h-8 w-48 bg-white/5 rounded animate-pulse mb-4" />
          <div className="h-12 w-96 bg-white/5 rounded animate-pulse" />
        </div>
      </div>
    );
  }

  if (!tool) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] text-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Tool not found</h1>
          <Link href="/tools">
            <motion.button 
              className="px-6 py-3 bg-[#0D7377] rounded-xl font-medium"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Back to Tools
            </motion.button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0D0D0D] text-white">
      {/* Grid Background */}
      <div className="fixed inset-0 pointer-events-none">
        <div 
          className="absolute inset-0 opacity-[0.02]"
          style={{
            backgroundImage: `
              linear-gradient(to right, #0D7377 1px, transparent 1px),
              linear-gradient(to bottom, #0D7377 1px, transparent 1px)
            `,
            backgroundSize: '60px 60px',
          }}
        />
      </div>

      {/* Header */}
      <header className="relative border-b border-white/5">
        <div className="max-w-5xl mx-auto px-6 pt-24 pb-12">
          <Link href="/tools" className="inline-flex items-center gap-2 text-white/40 hover:text-[#0D7377] transition-colors mb-8 group">
            <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
            Back to Tools
          </Link>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {/* Badges */}
            <div className="flex flex-wrap items-center gap-3 mb-4">
              <span className="px-3 py-1 text-sm font-mono text-[#0D7377] bg-[#0D7377]/10 border border-[#0D7377]/30 rounded-lg">
                {formatCategory(tool.category)}
              </span>
              <span className={cn(
                "px-3 py-1 text-sm font-medium rounded-lg border",
                pricingColors[tool.pricing]
              )}>
                {formatPricing(tool.pricing)}
              </span>
            </div>

            {/* Title */}
            <h1 className="text-4xl md:text-5xl font-black tracking-tight mb-2">
              {tool.name}
            </h1>
            <p className="text-lg text-white/50">by {tool.provider}</p>
          </motion.div>
        </div>
      </header>

      {/* Content */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="max-w-5xl mx-auto px-6 py-12"
      >
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main */}
          <div className="lg:col-span-2 space-y-8">
            {/* Description */}
            <section className="p-6 rounded-2xl bg-[#111111] border border-white/5">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 rounded-lg bg-[#0D7377]/10 border border-[#0D7377]/20">
                  <Layers className="w-5 h-5 text-[#0D7377]" />
                </div>
                <h2 className="text-xl font-bold">About</h2>
              </div>
              <p className="text-white/70 leading-relaxed">{tool.description}</p>
            </section>

            {/* Code */}
            <section className="rounded-2xl bg-[#111111] border border-white/5 overflow-hidden">
              <div className="flex items-center justify-between px-6 py-4 border-b border-white/5">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-[#0D7377]/10 border border-[#0D7377]/20">
                    <Terminal className="w-5 h-5 text-[#0D7377]" />
                  </div>
                  <h2 className="text-xl font-bold">Quick Start</h2>
                </div>
                <motion.button 
                  onClick={copyCode}
                  className="flex items-center gap-2 px-3 py-1.5 text-sm text-white/50 hover:text-[#0D7377] bg-white/5 hover:bg-[#0D7377]/10 rounded-lg transition-colors"
                  whileTap={{ scale: 0.95 }}
                >
                  {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                  {copied ? "Copied!" : "Copy"}
                </motion.button>
              </div>
              <pre className="p-6 overflow-x-auto">
                <code className="text-sm font-mono text-[#0D7377]">{tool.code_example}</code>
              </pre>
            </section>

            {/* Pros & Cons */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-6 rounded-2xl bg-emerald-500/5 border border-emerald-500/20">
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <Check className="w-5 h-5 text-emerald-400" />
                  Pros
                </h3>
                <ul className="space-y-3">
                  {tool.pros.map((pro, i) => (
                    <li key={i} className="flex items-start gap-3 text-white/70 text-sm">
                      <Check className="w-4 h-4 text-emerald-400 mt-0.5 shrink-0" />
                      {pro}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="p-6 rounded-2xl bg-rose-500/5 border border-rose-500/20">
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <X className="w-5 h-5 text-rose-400" />
                  Cons
                </h3>
                <ul className="space-y-3">
                  {tool.cons.map((con, i) => (
                    <li key={i} className="flex items-start gap-3 text-white/70 text-sm">
                      <X className="w-4 h-4 text-rose-400 mt-0.5 shrink-0" />
                      {con}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-4">
            {/* Links */}
            <div className="p-6 rounded-2xl bg-[#111111] border border-white/5">
              <h3 className="font-bold mb-4">Links</h3>
              <div className="space-y-2">
                <motion.a
                  href={tool.documentation_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-3 p-3 rounded-xl bg-white/5 hover:bg-[#0D7377]/10 border border-white/5 hover:border-[#0D7377]/30 transition-colors text-white/70 hover:text-[#0D7377]"
                  whileHover={{ x: 4 }}
                >
                  <ExternalLink className="w-4 h-4" />
                  Documentation
                </motion.a>
                {tool.github_url && (
                  <motion.a
                    href={tool.github_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-3 p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 hover:border-white/20 transition-colors text-white/70 hover:text-white"
                    whileHover={{ x: 4 }}
                  >
                    <Github className="w-4 h-4" />
                    GitHub
                  </motion.a>
                )}
              </div>
            </div>

            {/* Languages */}
            <div className="p-6 rounded-2xl bg-[#111111] border border-white/5">
              <h3 className="font-bold mb-4">Languages</h3>
              <div className="flex flex-wrap gap-2">
                {tool.languages.map((lang) => (
                  <span 
                    key={lang} 
                    className="px-3 py-1.5 text-sm bg-[#0D7377]/10 text-[#0D7377] border border-[#0D7377]/20 rounded-lg font-mono"
                  >
                    {lang}
                  </span>
                ))}
              </div>
            </div>

            {/* Alternatives */}
            {tool.alternatives.length > 0 && (
              <div className="p-6 rounded-2xl bg-[#111111] border border-white/5">
                <h3 className="font-bold mb-4">Alternatives</h3>
                <div className="space-y-2">
                  {tool.alternatives.map((alt) => (
                    <Link
                      key={alt}
                      href={`/tools/${alt.toLowerCase().replace(/\s+/g, "-")}`}
                      className="block p-3 rounded-xl bg-white/5 hover:bg-[#0D7377]/10 border border-white/5 hover:border-[#0D7377]/30 transition-colors text-white/70 hover:text-[#0D7377]"
                    >
                      {alt}
                    </Link>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
}
