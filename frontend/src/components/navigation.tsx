"use client";

import { Hexagon, Github, X, Search, Layers, Wrench } from "lucide-react";
import Link from "next/link";
import { useState, useEffect } from "react";

interface NavigationProps {
  onSearchClick?: () => void;
}

export function Navigation({ onSearchClick }: NavigationProps) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Close menu on escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") setIsMobileMenuOpen(false);
    };
    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, []);

  // Prevent body scroll when menu is open
  useEffect(() => {
    if (isMobileMenuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [isMobileMenuOpen]);

  const handleMobileSearchClick = () => {
    setIsMobileMenuOpen(false);
    onSearchClick?.();
  };

  return (
    <>
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

          {/* Right: GitHub (hidden on mobile to avoid clutter) */}
          <Link
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden md:block text-white/50 hover:text-amber-400 transition-colors"
          >
            <Github className="w-5 h-5" />
          </Link>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(true)}
            className="md:hidden text-white/70 hover:text-amber-400 p-2 -mr-2"
            aria-label="Open menu"
          >
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

      {/* Mobile Menu Overlay */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-[100] md:hidden">
          {/* Backdrop */}
          <div
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
            onClick={() => setIsMobileMenuOpen(false)}
          />

          {/* Drawer */}
          <div className="absolute right-0 top-0 h-full w-[280px] bg-[#0A0A12] border-l border-white/10 shadow-2xl animate-in slide-in-from-right duration-300">
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-white/10">
              <span className="text-lg font-semibold text-white font-heading">Menu</span>
              <button
                onClick={() => setIsMobileMenuOpen(false)}
                className="p-2 -mr-2 text-white/60 hover:text-white transition-colors"
                aria-label="Close menu"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Nav Links */}
            <div className="p-6 space-y-2">
              <Link
                href="/tools"
                onClick={() => setIsMobileMenuOpen(false)}
                className="flex items-center gap-3 p-3 rounded-lg text-white/80 hover:bg-amber-500/10 hover:text-amber-400 transition-all"
              >
                <Wrench className="w-5 h-5" />
                <span className="font-medium">Browse Tools</span>
              </Link>

              <button
                onClick={handleMobileSearchClick}
                className="flex items-center gap-3 p-3 rounded-lg text-white/80 hover:bg-amber-500/10 hover:text-amber-400 transition-all w-full text-left"
              >
                <Search className="w-5 h-5" />
                <span className="font-medium">Quick Search</span>
                <kbd className="ml-auto px-2 py-0.5 text-xs bg-white/10 border border-white/20 rounded font-mono">
                  ⌘K
                </kbd>
              </button>

              <Link
                href="/ask"
                onClick={() => setIsMobileMenuOpen(false)}
                className="flex items-center gap-3 p-3 rounded-lg text-white/80 hover:bg-violet-500/10 hover:text-violet-400 transition-all"
              >
                <Layers className="w-5 h-5" />
                <span className="font-medium">Consult AI</span>
              </Link>
            </div>

            {/* CTA */}
            <div className="p-6 border-t border-white/10">
              <Link
                href="/ask"
                onClick={() => setIsMobileMenuOpen(false)}
                className="flex items-center justify-center gap-2 w-full py-3 bg-gradient-to-r from-amber-500 to-amber-600 text-black rounded-lg font-semibold"
              >
                Start Consulting
                <span>→</span>
              </Link>
            </div>

            {/* Footer */}
            <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-white/10">
              <Link
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => setIsMobileMenuOpen(false)}
                className="flex items-center gap-3 text-white/50 hover:text-white transition-colors"
              >
                <Github className="w-5 h-5" />
                <span className="text-sm">View on GitHub</span>
              </Link>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
