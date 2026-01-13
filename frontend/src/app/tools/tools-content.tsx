"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowLeft, Search, Network, Database, Code2, Terminal, Activity, Cloud, Zap, ExternalLink, Github, Grid3X3 } from "lucide-react";
import Link from "next/link";
import { useSearchParams, useRouter } from "next/navigation";
import { API_URL, formatCategory, formatPricing, cn } from "@/lib/utils";
import type { AITool } from "@/types";

const categories = [
  { id: "all", name: "All Tools", icon: Grid3X3, count: 90 },
  { id: "mcp", name: "MCP Servers", icon: Network, count: 24 },
  { id: "api", name: "AI Models", icon: Zap, count: 18 },
  { id: "vector_db", name: "Vector DBs", icon: Database, count: 12 },
  { id: "agent_framework", name: "Agents", icon: Code2, count: 15 },
  { id: "cli", name: "CLI Tools", icon: Terminal, count: 8 },
  { id: "observability", name: "Observability", icon: Activity, count: 8 },
  { id: "deployment", name: "Deployment", icon: Cloud, count: 10 },
];

const pricingColors: Record<string, string> = {
  free: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30",
  freemium: "text-amber-400 bg-amber-500/10 border-amber-500/30",
  paid: "text-violet-400 bg-violet-500/10 border-violet-500/30",
  enterprise: "text-rose-400 bg-rose-500/10 border-rose-500/30",
};

function ToolCard({ tool, index }: { tool: AITool; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.4, delay: index * 0.03 }}
      layout
    >
      <Link href={`/tools/${tool.id}`}>
        <motion.div
          className="group relative h-full"
          whileHover={{ y: -6, scale: 1.01 }}
          transition={{ type: "spring", stiffness: 300, damping: 20 }}
        >
          {/* Animated gradient glow on hover */}
          <motion.div
            className="absolute -inset-[1px] rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"
            style={{
              background: 'linear-gradient(135deg, #0D7377 0%, #14B8A6 50%, #FF6B6B 100%)',
            }}
          />
          
          {/* Shine effect */}
          <motion.div
            className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 overflow-hidden"
            initial={false}
          >
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"
            />
          </motion.div>
          
          <div className="relative h-full p-6 rounded-2xl bg-black/40 backdrop-blur-md border border-white/[0.08] group-hover:border-white/[0.15] group-hover:bg-black/50 transition-all duration-300 overflow-hidden">
            {/* Subtle glass reflection */}
            <div className="absolute inset-0 bg-gradient-to-br from-white/[0.03] via-transparent to-transparent" />
            
            {/* Header */}
            <div className="relative flex items-start justify-between mb-4">
              <div>
                <h3 className="text-lg font-bold text-white group-hover:text-[#14B8A6] transition-colors duration-300">
                  {tool.name}
                </h3>
                <p className="text-sm text-white/40 group-hover:text-white/60 transition-colors">{tool.provider}</p>
              </div>
              <motion.span 
                className={cn(
                  "px-2.5 py-1 text-xs font-medium rounded-full border",
                  pricingColors[tool.pricing] || "text-white/60 bg-white/5 border-white/10"
                )}
                whileHover={{ scale: 1.05 }}
              >
                {formatPricing(tool.pricing)}
              </motion.span>
            </div>

            {/* Category badge */}
            <div className="relative flex items-center gap-2 mb-4">
              <motion.span 
                className="px-2.5 py-1 text-xs font-mono text-[#0D7377] bg-[#0D7377]/10 border border-[#0D7377]/20 rounded-lg"
                whileHover={{ scale: 1.05 }}
              >
                {formatCategory(tool.category)}
              </motion.span>
            </div>

            {/* Description */}
            <p className="relative text-sm text-white/50 group-hover:text-white/70 line-clamp-2 mb-4 leading-relaxed transition-colors">
              {tool.description}
            </p>

            {/* Languages with colorful badges */}
            <div className="relative flex flex-wrap gap-1.5 mb-4">
              {tool.languages.slice(0, 4).map((lang, i) => (
                <motion.span
                  key={lang}
                  className="text-xs px-2 py-0.5 rounded-md bg-white/5 text-white/50 font-mono group-hover:bg-white/10 group-hover:text-white/70 transition-colors"
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.03 + i * 0.05 }}
                >
                  {lang}
                </motion.span>
              ))}
              {tool.languages.length > 4 && (
                <span className="text-xs px-2 py-0.5 rounded-md bg-white/5 text-white/40">
                  +{tool.languages.length - 4}
                </span>
              )}
            </div>

            {/* Footer */}
            <div className="relative flex items-center gap-4 text-xs text-white/30 pt-4 border-t border-white/5 group-hover:border-white/10 transition-colors">
              <motion.span 
                className="flex items-center gap-1.5 group-hover:text-[#14B8A6] transition-colors"
                whileHover={{ x: 2 }}
              >
                <ExternalLink className="w-3.5 h-3.5" />
                Docs
              </motion.span>
              {tool.github_url && (
                <motion.span 
                  className="flex items-center gap-1.5 group-hover:text-white transition-colors"
                  whileHover={{ x: 2 }}
                >
                  <Github className="w-3.5 h-3.5" />
                  GitHub
                </motion.span>
              )}
            </div>
          </div>
        </motion.div>
      </Link>
    </motion.div>
  );
}

export default function ToolsContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const initialCategory = searchParams.get("category") || "all";
  
  const [tools, setTools] = useState<AITool[]>([]);
  const [selectedCategory, setSelectedCategory] = useState(initialCategory);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    const fetchTools = async () => {
      setIsLoading(true);
      try {
        const params = new URLSearchParams();
        if (selectedCategory !== "all") {
          params.set("category", selectedCategory);
        }
        params.set("limit", "50");

        const response = await fetch(`${API_URL}/api/tools?${params}`);
        if (response.ok) {
          const data = await response.json();
          setTools(data.tools);
        }
      } catch (error) {
        console.error("Error fetching tools:", error);
        setTools([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTools();
  }, [selectedCategory]);

  const filteredTools = searchQuery 
    ? tools.filter(t => 
        t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.description.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : tools;

  const handleCategoryChange = (catId: string) => {
    setSelectedCategory(catId);
    router.push(catId === "all" ? "/tools" : `/tools?category=${catId}`, { scroll: false });
  };

  return (
    <div className="min-h-screen bg-[#0A0A0A] text-white">
      {/* Subtle Background - Dark with grain texture */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        
        {/* Very subtle grain texture */}
        <svg className="absolute inset-0 w-full h-full opacity-[0.08]" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <filter id="grain">
              <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" stitchTiles="stitch" />
              <feColorMatrix type="saturate" values="0" />
            </filter>
          </defs>
          <rect width="100%" height="100%" filter="url(#grain)" />
        </svg>
        
        {/* Very faint static color wash - barely visible */}
        <div 
          className="absolute inset-0 opacity-[0.03]"
          style={{
            background: 'radial-gradient(ellipse at 20% 20%, rgba(13, 115, 119, 0.3) 0%, transparent 50%), radial-gradient(ellipse at 80% 80%, rgba(20, 184, 166, 0.2) 0%, transparent 50%)',
          }}
        />
        
        {/* Subtle grid pattern */}
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

      {/* Header with gradient flair */}
      <header className="relative border-b border-white/5 overflow-hidden">
        {/* Gradient backdrop */}
        <div className="absolute inset-0 bg-gradient-to-br from-[#0D7377]/20 via-transparent to-[#FF6B6B]/10" />
        
        {/* Animated orbs for depth */}
        <motion.div 
          className="absolute top-0 right-0 w-96 h-96 bg-[#0D7377]/30 rounded-full blur-3xl"
          animate={{ 
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div 
          className="absolute -bottom-20 left-1/4 w-64 h-64 bg-[#FF6B6B]/20 rounded-full blur-3xl"
          animate={{ 
            scale: [1, 1.3, 1],
            x: [0, 50, 0],
          }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
        
        <div className="relative max-w-7xl mx-auto px-6 pt-24 pb-12">
          <Link href="/" className="inline-flex items-center gap-2 text-white/40 hover:text-[#0D7377] transition-colors mb-8 group">
            <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
            Back
          </Link>
          
          {/* Enhanced title with glow */}
          <motion.div className="relative mb-4">
            {/* Title glow */}
            <motion.div 
              className="absolute -inset-4 bg-gradient-to-r from-[#0D7377]/40 to-[#14B8A6]/20 blur-2xl rounded-full"
              animate={{ opacity: [0.4, 0.7, 0.4] }}
              transition={{ duration: 3, repeat: Infinity }}
            />
            <motion.h1 
              className="relative text-5xl md:text-6xl font-black tracking-tighter"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <span className="text-white">Browse</span>{" "}
              <motion.span 
                className="relative"
                style={{ 
                  background: 'linear-gradient(90deg, #0D7377, #14B8A6, #0D7377)',
                  backgroundSize: '200% auto',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
                animate={{ backgroundPosition: ['0% center', '200% center'] }}
                transition={{ duration: 4, repeat: Infinity, ease: 'linear' }}
              >
                Tools
              </motion.span>
            </motion.h1>
          </motion.div>
          
          <motion.p 
            className="text-lg text-white/60 max-w-xl mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            Explore our complete index of AI development infrastructure.
          </motion.p>

          {/* Search with glow */}
          <motion.div 
            className="relative max-w-xl"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="absolute -inset-1 rounded-xl bg-gradient-to-r from-[#0D7377]/30 to-[#14B8A6]/20 blur-lg opacity-50" />
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/30" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search tools..."
                className="w-full pl-12 pr-4 py-4 bg-[#111111] border border-white/10 rounded-xl text-white placeholder:text-white/30 focus:outline-none focus:border-[#0D7377]/50 transition-colors"
              />
            </div>
          </motion.div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="flex flex-col lg:flex-row gap-8">
          
          {/* True Black Glass Sidebar */}
          <aside className="lg:w-72 shrink-0">
            <div className="lg:sticky lg:top-24">
              {/* True Black Glass Container */}
              <div className="relative p-5 rounded-2xl overflow-hidden">
                {/* Pure black base - no transparency */}
                <div className="absolute inset-0 bg-[#000000]" />
                
                {/* Very subtle grain texture for depth */}
                <div 
                  className="absolute inset-0 opacity-[0.04]"
                  style={{
                    backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 200 200\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noise\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.9\' numOctaves=\'4\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noise)\'/%3E%3C/svg%3E")',
                  }}
                />
                
                {/* Subtle vibrant ambient color wash - very faint */}
                <div 
                  className="absolute inset-0 opacity-20"
                  style={{
                    background: 'radial-gradient(ellipse at 20% 30%, rgba(13, 115, 119, 0.08) 0%, transparent 60%), radial-gradient(ellipse at 80% 70%, rgba(139, 92, 246, 0.06) 0%, transparent 60%)',
                  }}
                />
                
                {/* Glass border - clean line glow */}
                <div className="absolute inset-0 rounded-2xl border border-white/[0.06]" />
                <motion.div 
                  className="absolute inset-0 rounded-2xl"
                  style={{ 
                    border: '1px solid rgba(13, 115, 119, 0.15)',
                  }}
                  animate={{ 
                    borderColor: ['rgba(13, 115, 119, 0.1)', 'rgba(13, 115, 119, 0.25)', 'rgba(13, 115, 119, 0.1)']
                  }}
                  transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                />
                
                {/* Category content */}
                <div className="relative space-y-1">
                  <div className="flex items-center gap-2 mb-5 px-2">
                    <motion.div 
                      className="w-1.5 h-1.5 rounded-full bg-[#14B8A6]"
                      animate={{ opacity: [0.5, 1, 0.5] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    />
                    <p className="text-xs text-white/40 uppercase tracking-widest font-medium">Categories</p>
                  </div>
                  
                  {categories.map((cat, idx) => {
                    const Icon = cat.icon;
                    const isActive = selectedCategory === cat.id;
                    // Premium color palette for border glows
                    const colors = [
                      { bg: '#0D7377', border: '#0D7377' },
                      { bg: '#14B8A6', border: '#14B8A6' },
                      { bg: '#8B5CF6', border: '#8B5CF6' },
                      { bg: '#06B6D4', border: '#06B6D4' },
                      { bg: '#A78BFA', border: '#A78BFA' },
                      { bg: '#22D3EE', border: '#22D3EE' },
                      { bg: '#10B981', border: '#10B981' },
                      { bg: '#6366F1', border: '#6366F1' },
                    ];
                    const color = colors[idx % colors.length];
                    
                    return (
                      <motion.button
                        key={cat.id}
                        onClick={() => handleCategoryChange(cat.id)}
                        className="relative w-full group"
                        whileHover={{ x: isActive ? 0 : 2 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        {/* Active state - border glow line, not spread */}
                        {isActive && (
                          <motion.div 
                            className="absolute inset-0 rounded-xl"
                            style={{ 
                              border: `1px solid ${color.border}`,
                              background: `linear-gradient(135deg, ${color.bg}08, transparent 50%)`,
                            }}
                            layoutId="activeCategoryBorder"
                          />
                        )}
                        
                        {/* Hover border effect */}
                        <div 
                          className="absolute inset-0 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                          style={{ 
                            border: `1px solid ${color.border}40`,
                          }}
                        />
                        
                        {/* Button content */}
                        <div className={cn(
                          "relative flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-300",
                          isActive 
                            ? "bg-white/[0.02]"
                            : "bg-transparent hover:bg-white/[0.02]"
                        )}>
                          {/* Icon container */}
                          <div 
                            className={cn(
                              "relative w-8 h-8 rounded-lg flex items-center justify-center transition-all duration-300",
                              isActive ? "scale-100" : "group-hover:scale-105"
                            )}
                            style={{ 
                              background: isActive ? `${color.bg}15` : 'transparent',
                              border: isActive ? `1px solid ${color.border}40` : '1px solid rgba(255,255,255,0.04)'
                            }}
                          >
                            <Icon 
                              className="w-4 h-4 transition-all duration-300" 
                              style={{ 
                                color: isActive ? color.bg : 'rgba(255,255,255,0.4)',
                              }}
                            />
                          </div>
                          
                          {/* Label */}
                          <span className={cn(
                            "flex-1 text-sm font-medium text-left transition-colors duration-300",
                            isActive ? "text-white" : "text-white/50 group-hover:text-white/75"
                          )}>
                            {cat.name}
                          </span>
                          
                          {/* Count badge */}
                          <span 
                            className={cn(
                              "text-xs font-mono px-1.5 py-0.5 rounded transition-all duration-300",
                              isActive 
                                ? "text-white/80" 
                                : "text-white/25 group-hover:text-white/45"
                            )}
                            style={{
                              color: isActive ? color.bg : undefined
                            }}
                          >
                            {cat.count}
                          </span>
                        </div>
                      </motion.button>
                    );
                  })}
                </div>
              </div>
            </div>
          </aside>

          {/* Tools Grid */}
          <main className="flex-1">
            {/* Results count */}
            <div className="mb-6 flex items-center justify-between">
              <p className="text-sm text-white/40">
                {isLoading ? (
                  "Loading..."
                ) : (
                  <>
                    <span className="text-white font-medium">{filteredTools.length}</span> tools
                    {selectedCategory !== "all" && (
                      <> in <span className="text-[#0D7377]">{categories.find(c => c.id === selectedCategory)?.name}</span></>
                    )}
                  </>
                )}
              </p>
            </div>

            {/* Grid */}
            {isLoading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="h-64 rounded-2xl bg-[#111111] border border-white/5 animate-pulse" />
                ))}
              </div>
            ) : (
              <AnimatePresence mode="popLayout">
                <motion.div
                  key={selectedCategory + searchQuery}
                  className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4"
                >
                  {filteredTools.map((tool, index) => (
                    <ToolCard key={tool.id} tool={tool} index={index} />
                  ))}
                </motion.div>
              </AnimatePresence>
            )}

            {/* Empty state */}
            {!isLoading && filteredTools.length === 0 && (
              <div className="text-center py-20">
                <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-[#111111] flex items-center justify-center">
                  <Search className="w-8 h-8 text-white/20" />
                </div>
                <p className="text-white/50 mb-2">No tools found</p>
                <p className="text-sm text-white/30">Try adjusting your search or filter</p>
              </div>
            )}
          </main>
        </div>
      </div>
      
      {/* Bottom Flair Section - AI Luxury */}
      <section className="relative px-6 py-24 overflow-hidden">
        {/* Vibrant gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-[#0D7377]/20 via-[#0D0D0D] to-[#FF6B6B]/10" />
        
        {/* Animated floating orbs */}
        <motion.div 
          className="absolute top-0 left-1/4 w-80 h-80 bg-[#0D7377]/20 rounded-full blur-3xl"
          animate={{ 
            y: [0, -30, 0],
            scale: [1, 1.1, 1],
          }}
          transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div 
          className="absolute bottom-0 right-1/4 w-64 h-64 bg-[#FF6B6B]/15 rounded-full blur-3xl"
          animate={{ 
            y: [0, 30, 0],
            scale: [1, 1.2, 1],
          }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div 
          className="absolute top-1/2 right-0 w-48 h-48 bg-[#A78BFA]/15 rounded-full blur-3xl"
          animate={{ 
            x: [0, -20, 0],
          }}
          transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
        />
        
        {/* Animated diagonal lines */}
        <motion.div 
          className="absolute inset-0 opacity-[0.05]"
          style={{
            backgroundImage: 'repeating-linear-gradient(45deg, #14B8A6 0px, #14B8A6 1px, transparent 1px, transparent 40px)',
          }}
          animate={{ backgroundPosition: ['0px 0px', '40px 40px'] }}
          transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
        />
        
        <div className="relative max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            {/* Colorful badge */}
            <motion.div 
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-[#0D7377]/20 to-[#14B8A6]/20 border border-[#0D7377]/30 mb-6"
              whileHover={{ scale: 1.05 }}
            >
              <span className="w-2 h-2 rounded-full bg-[#14B8A6] animate-pulse" />
              <span className="text-sm text-[#14B8A6] font-medium">AI-Powered Discovery</span>
            </motion.div>
            
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              <span className="text-white">Let </span>
              <motion.span 
                className="bg-gradient-to-r from-[#0D7377] via-[#14B8A6] to-[#0D7377] bg-clip-text text-transparent"
                style={{ backgroundSize: '200% auto' }}
                animate={{ backgroundPosition: ['0% center', '200% center'] }}
                transition={{ duration: 4, repeat: Infinity, ease: 'linear' }}
              >
                AI
              </motion.span>
              <span className="text-white"> find your perfect tool</span>
            </h2>
            
            <p className="text-white/60 mb-10 max-w-xl mx-auto text-lg leading-relaxed">
              Get personalized recommendations for MCPs, APIs, CLIs, and SDKs based on your specific use case.
            </p>
            
            <Link href="/ask">
              <motion.button
                className="group inline-flex items-center gap-3 px-10 py-5 bg-gradient-to-r from-[#0D7377] via-[#14B8A6] to-[#0D7377] rounded-2xl font-bold text-white text-lg shadow-lg shadow-[#0D7377]/25"
                style={{ backgroundSize: '200% auto' }}
                whileHover={{ scale: 1.05, backgroundPosition: '100% center' }}
                whileTap={{ scale: 0.95 }}
                transition={{ duration: 0.3 }}
              >
                Consult AI
                <motion.div
                  animate={{ x: [0, 5, 0] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                >
                  <Zap className="w-5 h-5" />
                </motion.div>
              </motion.button>
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
