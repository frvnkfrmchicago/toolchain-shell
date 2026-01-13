"use client";

/**
 * SearchModal - Premium search experience with live agent progress
 *
 * Per skills-library-v2:
 * - agents/agentic-ux/SKILL.md: Show agent progress, transparency
 * - agents/micro-interactions/SKILL.md: Spring animations, loading states
 * - workflows/animation-planning/SKILL.md: Modal open/close timeline
 */

import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Search, Bot, Database, Globe, Brain, Loader2, ArrowRight } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { toast } from "sonner";
import { API_URL } from "@/lib/utils";
import { handleAPIError } from "@/lib/api-error-handler";

interface SearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialQuery?: string;
}

type AgentStatus = "idle" | "supervisor" | "search" | "rag" | "explain";

interface AgentInfo {
  id: AgentStatus;
  label: string;
  icon: React.ReactNode;
  description: string;
}

const agents: AgentInfo[] = [
  { id: "supervisor", label: "Router", icon: <Brain className="w-3.5 h-3.5" />, description: "Analyzing query..." },
  { id: "search", label: "Search", icon: <Globe className="w-3.5 h-3.5" />, description: "Searching web..." },
  { id: "rag", label: "Database", icon: <Database className="w-3.5 h-3.5" />, description: "Querying tools..." },
  { id: "explain", label: "Response", icon: <Bot className="w-3.5 h-3.5" />, description: "Generating..." },
];

export function SearchModal({ isOpen, onClose, initialQuery = "" }: SearchModalProps) {
  const [query, setQuery] = useState(initialQuery);
  const [isLoading, setIsLoading] = useState(false);
  const [currentAgent, setCurrentAgent] = useState<AgentStatus>("idle");
  const [messages, setMessages] = useState<string[]>([]);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Sync initial query when modal opens
  useEffect(() => {
    if (isOpen) {
      setQuery(initialQuery);
      // Auto-focus input after animation
      const timer = setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [isOpen, initialQuery]);

  // Reset state when modal closes
  useEffect(() => {
    if (!isOpen) {
      // Abort any in-flight request
      abortControllerRef.current?.abort();
      // Reset after close animation
      const timer = setTimeout(() => {
        setIsLoading(false);
        setCurrentAgent("idle");
        setMessages([]);
        setResult(null);
        setError(null);
      }, 200);
      return () => clearTimeout(timer);
    }
  }, [isOpen]);

  const handleSearch = useCallback(async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!query.trim() || isLoading) return;

    // Reset state
    setIsLoading(true);
    setResult(null);
    setError(null);
    setMessages([]);
    setCurrentAgent("supervisor");

    // Create abort controller for this request
    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(`${API_URL}/api/query/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query.trim() }),
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      if (!response.body) {
        throw new Error("No response body");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n").filter((line) => line.startsWith("data: "));

        for (const line of lines) {
          try {
            const jsonStr = line.slice(6); // Remove "data: " prefix
            if (jsonStr === "[DONE]" || jsonStr.includes('"done": true')) continue;

            const data = JSON.parse(jsonStr);

            // Update current agent based on node name
            if (data.node) {
              const agentMap: Record<string, AgentStatus> = {
                supervisor: "supervisor",
                search: "search",
                rag: "rag",
                explain: "explain",
              };
              const newAgent = agentMap[data.node];
              if (newAgent) {
                setCurrentAgent(newAgent);
              }
            }

            // Add messages to log
            if (data.messages && Array.isArray(data.messages)) {
              setMessages((prev) => [...prev, ...data.messages]);
            }

            // Set final response
            if (data.final_response) {
              setResult(data.final_response);
            }
          } catch {
            // Skip parse errors for malformed chunks
          }
        }
      }
    } catch (err) {
      const result = handleAPIError(err, () => handleSearch());

      if (result.shouldRetry) {
        setError(result.message);
      }
    } finally {
      setIsLoading(false);
      setCurrentAgent("idle");
    }
  }, [query, isLoading]);

  // Get current agent info
  const currentAgentInfo = agents.find((a) => a.id === currentAgent);

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="fixed inset-x-4 top-[10%] md:inset-x-auto md:left-1/2 md:-translate-x-1/2 md:w-full md:max-w-2xl z-50 flex flex-col max-h-[80vh] rounded-xl border border-white/10 bg-[#0A0A0F] shadow-2xl overflow-hidden"
          >
            {/* Search Input */}
            <form onSubmit={handleSearch} className="border-b border-white/10 p-4 shrink-0">
              <div className="flex items-center gap-3">
                {isLoading ? (
                  <Loader2 className="w-5 h-5 text-cyan-400 animate-spin" />
                ) : (
                  <Search className="w-5 h-5 text-white/40" />
                )}
                <input
                  ref={inputRef}
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask about AI tools..."
                  disabled={isLoading}
                  className="flex-1 bg-transparent text-white placeholder:text-white/30 focus:outline-none text-lg disabled:opacity-50"
                />
                <div className="flex items-center gap-2">
                  {query.trim() && !isLoading && (
                    <button
                      type="submit"
                      className="p-2 bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-400 rounded-lg transition-colors"
                    >
                      <ArrowRight className="w-4 h-4" />
                    </button>
                  )}
                  <button
                    type="button"
                    onClick={onClose}
                    className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                  >
                    <X className="w-4 h-4 text-white/40" />
                  </button>
                </div>
              </div>
            </form>

            {/* Agent Progress - Per agentic-ux/SKILL.md: Show agent progress */}
            {isLoading && (
              <div className="p-4 border-b border-white/10 shrink-0">
                {/* Agent Pipeline */}
                <div className="flex items-center gap-2 mb-3">
                  {agents.map((agent, index) => (
                    <div key={agent.id} className="flex items-center">
                      <div
                        className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-mono uppercase tracking-wider transition-all duration-300 ${
                          currentAgent === agent.id
                            ? "bg-cyan-500/20 text-cyan-400 ring-1 ring-cyan-500/50 shadow-lg shadow-cyan-500/20"
                            : agents.findIndex((a) => a.id === currentAgent) > index
                              ? "bg-green-500/10 text-green-400/60"
                              : "bg-white/5 text-white/30"
                        }`}
                      >
                        {agent.icon}
                        <span className="hidden sm:inline">{agent.label}</span>
                      </div>
                      {index < agents.length - 1 && (
                        <div className="w-4 h-px bg-white/10 mx-1" />
                      )}
                    </div>
                  ))}
                </div>

                {/* Current Agent Status */}
                {currentAgentInfo && (
                  <div className="text-xs text-white/50 font-mono">
                    {currentAgentInfo.description}
                  </div>
                )}

                {/* Live Messages */}
                {messages.length > 0 && (
                  <div className="mt-3 space-y-1 text-[11px] text-white/40 font-mono max-h-20 overflow-y-auto">
                    {messages.slice(-5).map((msg, i) => (
                      <div key={i} className="truncate">
                        {msg}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Error State */}
            {error && !isLoading && (
              <div className="p-4 border-b border-red-500/20 bg-red-500/5 shrink-0">
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-full bg-red-500/20 flex items-center justify-center shrink-0">
                    <X className="w-4 h-4 text-red-400" />
                  </div>
                  <div>
                    <p className="text-sm text-red-400 font-medium">Request Failed</p>
                    <p className="text-xs text-red-400/60 mt-1">{error}</p>
                    <button
                      onClick={() => handleSearch()}
                      className="mt-2 text-xs text-cyan-400 hover:underline"
                    >
                      Try again
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Results */}
            {result && (
              <div className="flex-1 overflow-y-auto p-4">
                <div className="prose prose-invert prose-sm max-w-none prose-headings:text-white prose-p:text-white/80 prose-strong:text-white prose-code:text-cyan-400 prose-code:bg-white/5 prose-code:px-1 prose-code:py-0.5 prose-code:rounded prose-pre:bg-white/5 prose-pre:border prose-pre:border-white/10">
                  <ReactMarkdown>{result}</ReactMarkdown>
                </div>
              </div>
            )}

            {/* Empty State */}
            {!isLoading && !result && !error && (
              <div className="flex-1 flex items-center justify-center p-8">
                <div className="text-center">
                  <div className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4">
                    <Search className="w-6 h-6 text-white/20" />
                  </div>
                  <p className="text-white/40 text-sm">
                    Ask anything about AI tools, frameworks, or APIs
                  </p>
                  <div className="flex flex-wrap gap-2 justify-center mt-4">
                    {["Best vector database?", "Compare LangChain vs LlamaIndex", "What is an MCP?"].map((suggestion) => (
                      <button
                        key={suggestion}
                        onClick={() => {
                          setQuery(suggestion);
                          // Auto-submit after setting query
                          setTimeout(() => handleSearch(), 0);
                        }}
                        className="px-3 py-1.5 text-xs text-white/50 bg-white/5 hover:bg-white/10 rounded-full transition-colors"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Footer */}
            <div className="p-3 border-t border-white/10 flex items-center justify-between text-[10px] text-white/30 font-mono shrink-0">
              <span>Press Enter to search</span>
              <span>ESC to close</span>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
