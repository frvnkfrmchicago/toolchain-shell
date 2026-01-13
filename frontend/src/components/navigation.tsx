"use client";

import { Hexagon, Github } from "lucide-react";
import Link from "next/link";
import { useState, useEffect } from "react";

interface NavigationProps {
  onSearchClick?: () => void;
}

export function Navigation({ onSearchClick }: NavigationProps) {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? "bg-[#0A0A12]/95 backdrop-blur-xl border-b border-white/10 shadow-lg"
          : "bg-[#0A0A12]/70 backdrop-blur-md border-b border-white/5"
      }`}
    >
      <div className="container px-6 py-4 flex items-center justify-between max-w-6xl mx-auto">
        {/* Logo Left */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-amber-500 to-amber-600 flex items-center justify-center group-hover:scale-110 transition-transform shadow-lg shadow-amber-500/20">
            <Hexagon className="w-5 h-5 text-black" />
          </div>
          <span className="text-2xl font-bold tracking-tight text-white font-heading">
            ToolChainDev
          </span>
        </Link>

        {/* Center Nav */}
        <div className="hidden md:flex items-center gap-8">
          <Link
            href="/tools"
            className="text-white/70 hover:text-amber-400 transition-colors font-medium"
          >
            Browse Tools
          </Link>
          <button
            onClick={onSearchClick}
            className="flex items-center gap-2 text-white/70 hover:text-amber-400 transition-colors font-medium group"
          >
            <span>Quick Search</span>
            <kbd className="px-2 py-0.5 text-xs bg-white/10 border border-white/20 rounded font-mono group-hover:border-amber-500/50 transition-colors">
              ⌘K
            </kbd>
          </button>
          <Link
            href="/ask"
            className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-amber-500 to-amber-600 text-black rounded-lg font-semibold hover:shadow-lg hover:shadow-amber-500/30 transition-all"
          >
            Consult
            <span className="text-sm">→</span>
          </Link>
        </div>

        {/* Right: GitHub */}
        <Link
          href="https://github.com"
          target="_blank"
          rel="noopener noreferrer"
          className="text-white/50 hover:text-amber-400 transition-colors"
        >
          <Github className="w-5 h-5" />
        </Link>

        {/* Mobile Menu Button */}
        <button className="md:hidden text-white/70 hover:text-amber-400">
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>
      </div>
    </nav>
  );
}
