"use client";

import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Send, Hexagon, Terminal, Database, Network, Code2, Github, ArrowRight } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";


gsap.registerPlugin(ScrollTrigger);

// Terminal demo messages
const demoQueries = [
  { query: "Best MCP server for PostgreSQL?", response: "supabase-mcp, pg-vector-mcp" },
  { query: "Compare Pinecone vs Weaviate", response: "Pinecone: fastest, Weaviate: open-source" },
  { query: "Top agent frameworks 2026?", response: "CrewAI, LangGraph, AutoGen" },
];

// Floating orb component
function FloatingOrb({ className, delay = 0 }: { className: string; delay?: number }) {
  return (
    <motion.div
      className={`absolute rounded-full blur-3xl pointer-events-none ${className}`}
      animate={{
        y: [0, -30, 0],
        x: [0, 20, 0],
        scale: [1, 1.1, 1],
      }}
      transition={{
        duration: 8,
        repeat: Infinity,
        delay,
        ease: "easeInOut",
      }}
    />
  );
}

// Animated grid background
function GridBackground() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {/* Grid lines */}
      <div 
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `
            linear-gradient(to right, #0D7377 1px, transparent 1px),
            linear-gradient(to bottom, #0D7377 1px, transparent 1px)
          `,
          backgroundSize: '60px 60px',
        }}
      />
      {/* Radial fade */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#0D0D0D]/50 to-[#0D0D0D]" />
    </div>
  );
}

// Glowing cursor trail for input
function GlowInput({ value, onChange, onSubmit }: { value: string; onChange: (v: string) => void; onSubmit: () => void }) {
  const [isFocused, setIsFocused] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const typingTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
    setIsTyping(true);
    
    // Reset typing state after 500ms of no input
    if (typingTimeoutRef.current) clearTimeout(typingTimeoutRef.current);
    typingTimeoutRef.current = setTimeout(() => setIsTyping(false), 500);
  };

  return (
    <div className="relative group">
      {/* Idle pulsing glow - always visible when not focused */}
      <motion.div 
        className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-[#0D7377]/30 to-[#14B8A6]/30 blur-xl"
        animate={{ 
          opacity: isFocused ? 0 : [0.15, 0.3, 0.15],
        }}
        transition={{ 
          duration: 2, 
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      
      {/* Focus glow - bright teal when focused */}
      <motion.div 
        className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-[#0D7377] via-[#14B8A6] to-[#0D7377] blur-xl"
        animate={{ opacity: isFocused ? 0.5 : 0 }}
        transition={{ duration: 0.3 }}
      />
      
      {/* Animated rotating gradient border while typing */}
      <motion.div 
        className="absolute -inset-px rounded-2xl overflow-hidden"
        animate={{ opacity: isTyping ? 1 : isFocused ? 0.6 : 0 }}
        transition={{ duration: 0.2 }}
      >
        <motion.div
          className="absolute inset-0"
          style={{
            background: 'conic-gradient(from 0deg, #0D7377, #FF6B6B, #0D7377, #14B8A6, #0D7377)',
          }}
          animate={{ 
            rotate: isTyping ? 360 : 0 
          }}
          transition={{ 
            duration: 2, 
            repeat: isTyping ? Infinity : 0,
            ease: "linear"
          }}
        />
        <div className="absolute inset-[2px] rounded-2xl bg-[#0D0D0D]" />
      </motion.div>
      
      <div className="relative flex items-center bg-[#0D0D0D] rounded-2xl overflow-hidden border border-white/5">
        <input
          type="text"
          value={value}
          onChange={handleChange}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          onKeyDown={(e) => e.key === 'Enter' && onSubmit()}
          placeholder="Ask about any AI tool..."
          className="flex-1 px-6 py-5 bg-transparent text-lg placeholder:text-white/30 focus:outline-none"
        />
        <motion.button
          onClick={onSubmit}
          className="m-2 p-4 bg-[#0D7377] rounded-xl"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Send className="w-5 h-5" />
        </motion.button>
      </div>
    </div>
  );
}

// Morphing terminal command component
function MorphingCommand({ commands, className, color, delay = 0 }: { commands: string[]; className: string; color: string; delay?: number }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % commands.length);
    }, 3000);
    return () => clearInterval(interval);
  }, [commands.length]);
  
  return (
    <motion.div 
      className={`${className} px-4 py-2 rounded-xl bg-black/80 border backdrop-blur-sm font-mono text-xs whitespace-nowrap overflow-hidden`}
      style={{ 
        borderColor: `${color}40`,
        boxShadow: `0 0 20px ${color}15`,
      }}
      animate={{ 
        y: [0, -10, 0],
        opacity: [0.7, 1, 0.7],
      }}
      transition={{ duration: 5, repeat: Infinity, delay, ease: "easeInOut" }}
    >
      <span style={{ color: `${color}` }} className="mr-1">$</span>
      <motion.span
        key={currentIndex}
        className="text-white/70"
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={{ duration: 0.4 }}
      >
        {commands[currentIndex]}
      </motion.span>
    </motion.div>
  );
}


export default function Home() {
  const container = useRef(null);
  const [inputValue, setInputValue] = useState("");
  const [demoIndex, setDemoIndex] = useState(0);
  const [typedText, setTypedText] = useState("");
  const [showDemo, setShowDemo] = useState(false);
  const router = useRouter();

  // Typing animation for demo
  useEffect(() => {
    if (!showDemo) return;
    const query = demoQueries[demoIndex].query;
    let i = 0;
    const interval = setInterval(() => {
      if (i <= query.length) {
        setTypedText(query.slice(0, i));
        i++;
      } else {
        clearInterval(interval);
        setTimeout(() => {
          setDemoIndex((prev) => (prev + 1) % demoQueries.length);
        }, 3000);
      }
    }, 40);
    return () => clearInterval(interval);
  }, [demoIndex, showDemo]);

  // GSAP animations
  useGSAP(() => {
    // Hero text reveal
    gsap.from(".hero-line", {
      y: 100,
      opacity: 0,
      duration: 1,
      stagger: 0.15,
      ease: "power4.out",
    });

    // Scroll-triggered demo
    ScrollTrigger.create({
      trigger: ".demo-card",
      start: "top 70%",
      onEnter: () => setShowDemo(true),
    });

    // Bento cards stagger
    gsap.from(".bento-card", {
      scrollTrigger: {
        trigger: ".bento-section",
        start: "top 80%",
      },
      y: 60,
      opacity: 0,
      duration: 0.8,
      stagger: 0.1,
      ease: "power3.out",
    });

    // Parallax on scroll
    gsap.to(".floating-orb-1", {
      scrollTrigger: {
        trigger: container.current,
        start: "top top",
        end: "bottom top",
        scrub: 1,
      },
      y: -200,
    });

    gsap.to(".floating-orb-2", {
      scrollTrigger: {
        trigger: container.current,
        start: "top top",
        end: "bottom top",
        scrub: 1,
      },
      y: -100,
    });

  }, { scope: container });

  const handleSubmit = () => {
    if (inputValue.trim()) {
      router.push(`/ask?q=${encodeURIComponent(inputValue.trim())}`);
    }
  };

  return (
    <main ref={container} className="bg-[#0D0D0D] min-h-screen text-white overflow-x-hidden">
      {/* Background Effects */}
      <GridBackground />
      <FloatingOrb className="floating-orb-1 w-96 h-96 bg-[#0D7377]/30 top-20 -left-48" delay={0} />
      <FloatingOrb className="floating-orb-2 w-80 h-80 bg-[#FF6B6B]/20 top-96 -right-40" delay={2} />

      {/* NAVIGATION */}
      <nav className="fixed top-0 left-0 right-0 z-50 px-6 py-4 backdrop-blur-xl bg-[#0D0D0D]/80">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <motion.div
              className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#0D7377] to-[#0A5F62] flex items-center justify-center"
              whileHover={{ rotate: 180 }}
              transition={{ duration: 0.5 }}
            >
              <Hexagon className="w-4 h-4 text-white" />
            </motion.div>
            <span className="text-xl font-black tracking-tighter">TOOLCHAINDEV</span>
          </Link>
          <div className="flex items-center gap-6">
            <Link href="/tools" className="text-sm text-white/60 hover:text-white transition-colors">
              Browse Tools
            </Link>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Link 
                href="/ask"
                className="px-5 py-2.5 bg-gradient-to-r from-[#0D7377] to-[#0A5F62] text-white text-sm font-medium rounded-full"
              >
                Consult AI
              </Link>
            </motion.div>
          </div>
        </div>
      </nav>

      {/* HERO */}
      <section className="relative min-h-screen flex flex-col justify-center px-6 pt-20">
        <div className="max-w-7xl mx-auto w-full">
          {/* Typography */}
          <h1 className="text-[13vw] md:text-[11vw] lg:text-[9vw] font-black leading-[0.85] tracking-tighter mb-8">
            <span className="hero-line block overflow-hidden">
              <span className="block text-white">THE AI</span>
            </span>
            <span className="hero-line block overflow-hidden">
              <motion.span 
                className="block"
                style={{ 
                  background: 'linear-gradient(90deg, #0D7377, #14B8A6, #0D7377)',
                  backgroundSize: '200% auto',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
                animate={{ backgroundPosition: ['0% center', '200% center'] }}
                transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
              >
                DEVELOPER&apos;S
              </motion.span>
            </span>
            <span className="hero-line block overflow-hidden">
              <span className="block text-white/20">INDEX</span>
            </span>
          </h1>

          {/* Input */}
          <div className="max-w-2xl mb-10">
            <GlowInput value={inputValue} onChange={setInputValue} onSubmit={handleSubmit} />
            
            {/* Improved helper text */}
            <p className="text-base text-white/60 mt-6 max-w-xl leading-relaxed">
              Discover the right tools for your AI stack — <span className="text-[#0D7377] font-medium">MCPs, CLIs, APIs, and SDKs</span> — all indexed and explained.
            </p>
            
            {/* Prominent Browse CTA */}
            <motion.div 
              className="mt-6"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              <Link href="/tools">
                <motion.button 
                  className="inline-flex items-center gap-3 px-8 py-4 bg-white/5 border border-white/10 rounded-xl text-white font-medium hover:bg-white/10 hover:border-white/20 transition-all"
                  whileHover={{ scale: 1.02, x: 4 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <span>Browse 90+ Tools</span>
                  <ArrowRight className="w-4 h-4" />
                </motion.button>
              </Link>
            </motion.div>
          </div>
          
          {/* Educational Explainer Cards - Premium AI Luxury */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 max-w-5xl mb-12">
            {/* MCP Card */}
            <motion.div 
              className="group relative p-6 rounded-2xl bg-gradient-to-br from-[#0D7377]/10 to-transparent border border-[#0D7377]/20 overflow-hidden cursor-pointer"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              whileHover={{ scale: 1.02, y: -4 }}
            >
              {/* Glow effect on hover */}
              <motion.div 
                className="absolute inset-0 bg-gradient-to-br from-[#0D7377]/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              />
              <div className="relative">
                <motion.div 
                  className="w-10 h-10 rounded-xl bg-[#0D7377]/20 border border-[#0D7377]/30 flex items-center justify-center mb-4"
                  whileHover={{ rotate: 10 }}
                >
                  <Network className="w-5 h-5 text-[#0D7377]" />
                </motion.div>
                <h3 className="font-bold mb-2 text-white group-hover:text-[#0D7377] transition-colors">MCP Servers</h3>
                <p className="text-sm text-white/50 leading-relaxed">Bridge AI to databases, APIs, and external data sources securely.</p>
              </div>
            </motion.div>
            
            {/* CLI Card */}
            <motion.div 
              className="group relative p-6 rounded-2xl bg-gradient-to-br from-[#14B8A6]/10 to-transparent border border-[#14B8A6]/20 overflow-hidden cursor-pointer"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 }}
              whileHover={{ scale: 1.02, y: -4 }}
            >
              <motion.div 
                className="absolute inset-0 bg-gradient-to-br from-[#14B8A6]/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              />
              <div className="relative">
                <motion.div 
                  className="w-10 h-10 rounded-xl bg-[#14B8A6]/20 border border-[#14B8A6]/30 flex items-center justify-center mb-4"
                  whileHover={{ rotate: 10 }}
                >
                  <Terminal className="w-5 h-5 text-[#14B8A6]" />
                </motion.div>
                <h3 className="font-bold mb-2 text-white group-hover:text-[#14B8A6] transition-colors">CLI Tools</h3>
                <p className="text-sm text-white/50 leading-relaxed">Command-line interfaces for AI workflows and automation.</p>
              </div>
            </motion.div>
            
            {/* Vector DB Card */}
            <motion.div 
              className="group relative p-6 rounded-2xl bg-gradient-to-br from-[#FF6B6B]/10 to-transparent border border-[#FF6B6B]/20 overflow-hidden cursor-pointer"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
              whileHover={{ scale: 1.02, y: -4 }}
            >
              <motion.div 
                className="absolute inset-0 bg-gradient-to-br from-[#FF6B6B]/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              />
              <div className="relative">
                <motion.div 
                  className="w-10 h-10 rounded-xl bg-[#FF6B6B]/20 border border-[#FF6B6B]/30 flex items-center justify-center mb-4"
                  whileHover={{ rotate: 10 }}
                >
                  <Database className="w-5 h-5 text-[#FF6B6B]" />
                </motion.div>
                <h3 className="font-bold mb-2 text-white group-hover:text-[#FF6B6B] transition-colors">Vector DBs</h3>
                <p className="text-sm text-white/50 leading-relaxed">Store embeddings for semantic search and RAG pipelines.</p>
              </div>
            </motion.div>
            
            {/* Frameworks Card */}
            <motion.div 
              className="group relative p-6 rounded-2xl bg-gradient-to-br from-[#A78BFA]/10 to-transparent border border-[#A78BFA]/20 overflow-hidden cursor-pointer"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.9 }}
              whileHover={{ scale: 1.02, y: -4 }}
            >
              <motion.div 
                className="absolute inset-0 bg-gradient-to-br from-[#A78BFA]/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              />
              <div className="relative">
                <motion.div 
                  className="w-10 h-10 rounded-xl bg-[#A78BFA]/20 border border-[#A78BFA]/30 flex items-center justify-center mb-4"
                  whileHover={{ rotate: 10 }}
                >
                  <Code2 className="w-5 h-5 text-[#A78BFA]" />
                </motion.div>
                <h3 className="font-bold mb-2 text-white group-hover:text-[#A78BFA] transition-colors">Agent Frameworks</h3>
                <p className="text-sm text-white/50 leading-relaxed">Build autonomous AI that reasons and executes tasks.</p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* YOUR AI JOURNEY SECTION */}
      <section className="relative px-6 py-32 overflow-hidden">
        {/* Vibrant gradient background */}
        <div className="absolute inset-0 bg-gradient-to-b from-[#0D0D0D] via-[#0D7377]/10 to-[#0D0D0D]" />
        
        {/* Morphing floating terminal commands */}
        <MorphingCommand 
          commands={['npx create-mcp', 'pip install langchain', 'bun add openai']}
          className="absolute top-20 left-[10%]"
          color="#0D7377"
          delay={0}
        />
        <MorphingCommand 
          commands={['docker run chroma', 'npx prisma generate', 'supabase start']}
          className="absolute top-40 right-[15%]"
          color="#FF6B6B"
          delay={2}
        />
        <MorphingCommand 
          commands={['crewai run', 'autogen build', 'langgraph compile']}
          className="absolute bottom-32 left-[20%]"
          color="#A78BFA"
          delay={4}
        />
        <MorphingCommand 
          commands={['ollama serve', 'vllm start', 'tgi launch']}
          className="absolute bottom-20 right-[25%]"
          color="#14B8A6"
          delay={1}
        />
        
        <div className="relative max-w-6xl mx-auto">
          {/* Section header */}
          <motion.div 
            className="text-center mb-20"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <motion.div 
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-[#0D7377]/20 to-[#14B8A6]/10 border border-[#0D7377]/30 mb-6"
              whileHover={{ scale: 1.05 }}
            >
              <span className="w-2 h-2 rounded-full bg-[#14B8A6] animate-pulse" />
              <span className="text-sm text-[#14B8A6] font-medium">Your Agent AI Journey</span>
            </motion.div>
            
            <h2 className="text-4xl md:text-6xl font-black mb-6">
              <span className="text-white">From Idea to </span>
              <motion.span 
                className="bg-gradient-to-r from-[#0D7377] via-[#14B8A6] to-[#FF6B6B] bg-clip-text text-transparent"
                style={{ backgroundSize: '200% auto' }}
                animate={{ backgroundPosition: ['0% center', '200% center'] }}
                transition={{ duration: 5, repeat: Infinity, ease: 'linear' }}
              >
                Production
              </motion.span>
            </h2>
            <p className="text-xl text-white/60 max-w-2xl mx-auto">
              ToolChainDev guides you through every step of building with AI infrastructure
            </p>
          </motion.div>

          {/* Journey Steps */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
            {/* Step 1: Discover */}
            <motion.div 
              className="group relative"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
            >
              <div className="absolute -inset-px rounded-3xl bg-gradient-to-br from-[#0D7377] to-[#0D7377]/50 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="relative p-8 rounded-3xl bg-[#111111] border border-white/5 h-full">
                <div className="flex items-center gap-4 mb-6">
                  <motion.div 
                    className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#0D7377]/30 to-[#0D7377]/10 border border-[#0D7377]/30 flex items-center justify-center"
                    whileHover={{ scale: 1.1, rotate: 5 }}
                  >
                    <span className="text-3xl font-black text-[#0D7377]">1</span>
                  </motion.div>
                  <div>
                    <span className="text-xs text-[#0D7377] font-mono">STEP ONE</span>
                    <h3 className="text-2xl font-bold">Discover</h3>
                  </div>
                </div>
                <p className="text-white/60 leading-relaxed mb-6">
                  Explore 90+ tools across MCPs, APIs, CLIs, and SDKs. Find exactly what your AI stack needs.
                </p>
                <div className="flex flex-wrap gap-2">
                  {['MCP Servers', 'Vector DBs', 'LLM APIs'].map((tag) => (
                    <span key={tag} className="px-3 py-1 text-xs bg-[#0D7377]/10 text-[#0D7377] rounded-full border border-[#0D7377]/20">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
            
            {/* Step 2: Compare */}
            <motion.div 
              className="group relative"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
            >
              <div className="absolute -inset-px rounded-3xl bg-gradient-to-br from-[#14B8A6] to-[#14B8A6]/50 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="relative p-8 rounded-3xl bg-[#111111] border border-white/5 h-full">
                <div className="flex items-center gap-4 mb-6">
                  <motion.div 
                    className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#14B8A6]/30 to-[#14B8A6]/10 border border-[#14B8A6]/30 flex items-center justify-center"
                    whileHover={{ scale: 1.1, rotate: 5 }}
                  >
                    <span className="text-3xl font-black text-[#14B8A6]">2</span>
                  </motion.div>
                  <div>
                    <span className="text-xs text-[#14B8A6] font-mono">STEP TWO</span>
                    <h3 className="text-2xl font-bold">Compare</h3>
                  </div>
                </div>
                <p className="text-white/60 leading-relaxed mb-6">
                  Let AI analyze trade-offs. Get personalized recommendations for your specific use case.
                </p>
                <div className="flex flex-wrap gap-2">
                  {['Side-by-side', 'Pricing', 'Features'].map((tag) => (
                    <span key={tag} className="px-3 py-1 text-xs bg-[#14B8A6]/10 text-[#14B8A6] rounded-full border border-[#14B8A6]/20">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
            
            {/* Step 3: Build */}
            <motion.div 
              className="group relative"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
            >
              <div className="absolute -inset-px rounded-3xl bg-gradient-to-br from-[#FF6B6B] to-[#FF6B6B]/50 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="relative p-8 rounded-3xl bg-[#111111] border border-white/5 h-full">
                <div className="flex items-center gap-4 mb-6">
                  <motion.div 
                    className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#FF6B6B]/30 to-[#FF6B6B]/10 border border-[#FF6B6B]/30 flex items-center justify-center"
                    whileHover={{ scale: 1.1, rotate: 5 }}
                  >
                    <span className="text-3xl font-black text-[#FF6B6B]">3</span>
                  </motion.div>
                  <div>
                    <span className="text-xs text-[#FF6B6B] font-mono">STEP THREE</span>
                    <h3 className="text-2xl font-bold">Build</h3>
                  </div>
                </div>
                <p className="text-white/60 leading-relaxed mb-6">
                  Ship your AI agents with confidence. Documentation, quickstarts, and best practices included.
                </p>
                <div className="flex flex-wrap gap-2">
                  {['Quickstart', 'Guides', 'Examples'].map((tag) => (
                    <span key={tag} className="px-3 py-1 text-xs bg-[#FF6B6B]/10 text-[#FF6B6B] rounded-full border border-[#FF6B6B]/20">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>
          
          {/* Enhanced Terminal Demo */}
          <motion.div 
            className="relative max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            {/* Terminal glow */}
            <div className="absolute -inset-4 bg-gradient-to-r from-[#0D7377]/20 via-[#14B8A6]/10 to-[#FF6B6B]/20 blur-2xl rounded-3xl" />
            
            <div className="relative rounded-2xl bg-[#0A0A0A] border border-white/10 overflow-hidden">
              {/* Terminal header */}
              <div className="flex items-center gap-2 px-4 py-3 bg-white/5 border-b border-white/5">
                <motion.div className="w-3 h-3 rounded-full bg-[#FF6B6B]" animate={{ scale: [1, 1.2, 1] }} transition={{ duration: 2, repeat: Infinity }} />
                <div className="w-3 h-3 rounded-full bg-[#F5F5DC]" />
                <div className="w-3 h-3 rounded-full bg-[#0D7377]" />
                <span className="ml-auto text-xs text-white/30 font-mono">toolchain-ai ~/projects</span>
              </div>
              
              {/* Terminal content */}
              <div className="p-6 font-mono text-sm space-y-4">
                <div className="flex items-start gap-3">
                  <span className="text-[#14B8A6]">→</span>
                  <div>
                    <span className="text-white/70">{typedText}</span>
                    {showDemo && <motion.span className="text-[#14B8A6]" animate={{ opacity: [1, 0] }} transition={{ duration: 0.5, repeat: Infinity }}>▋</motion.span>}
                  </div>
                </div>
                
                {typedText === demoQueries[demoIndex].query && (
                  <motion.div 
                    className="pl-6 space-y-2"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                  >
                    <div className="text-[#0D7377]">
                      <span className="text-white/40">AI:</span> {demoQueries[demoIndex].response}
                    </div>
                    <motion.div 
                      className="flex items-center gap-2 text-xs text-white/30"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.5 }}
                    >
                      <span className="w-1.5 h-1.5 rounded-full bg-[#14B8A6] animate-pulse" />
                      Powered by ToolChainDev AI
                    </motion.div>
                  </motion.div>
                )}
              </div>
            </div>
          </motion.div>
          
          {/* CTA */}
          <motion.div 
            className="text-center mt-16"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <Link href="/ask">
              <motion.button
                className="inline-flex items-center gap-3 px-10 py-5 bg-gradient-to-r from-[#0D7377] via-[#14B8A6] to-[#0D7377] rounded-2xl font-bold text-white text-lg shadow-lg shadow-[#0D7377]/25"
                style={{ backgroundSize: '200% auto' }}
                whileHover={{ scale: 1.05, backgroundPosition: '100% center' }}
                whileTap={{ scale: 0.95 }}
              >
                Start Your Journey
                <motion.div animate={{ x: [0, 5, 0] }} transition={{ duration: 1.5, repeat: Infinity }}>
                  <ArrowRight className="w-5 h-5" />
                </motion.div>
              </motion.button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="px-6 py-12 border-t border-white/5">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
          <span className="text-sm text-white/40">© 2026 ToolChainDev</span>
          <div className="flex items-center gap-6 text-sm text-white/40">
            <Link href="/tools" className="hover:text-white transition-colors">Tools</Link>
            <Link href="/ask" className="hover:text-white transition-colors">Consult</Link>
            <Link href="https://github.com" className="hover:text-white transition-colors">
              <Github className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </footer>
    </main>
  );
}
