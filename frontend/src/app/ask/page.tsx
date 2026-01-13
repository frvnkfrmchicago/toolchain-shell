"use client";

/**
 * Ask Page - Enhanced Design
 * 
 * Features:
 * - Subtle floating orbs background animation
 * - Fixed scroll issue
 * - Tech icons (Cpu, Network, Workflow) instead of robot/sparkles
 * - Better response formatting with cards
 */

import { useState, useRef, useEffect, Suspense, useCallback } from "react";
import { useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  Hexagon,
  User,
  Send,
  Loader2,
  Database,
  Layers,
  Network,
  Workflow,
  ArrowLeft
} from "lucide-react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Link from "next/link";
import { API_URL } from "@/lib/utils";
import { handleAPIError } from "@/lib/api-error-handler";
import { FloatingOrbs } from "@/components/ui/floating-orbs";

interface Message {
  role: "user" | "assistant";
  content: string;
  id: string;
  isStreaming?: boolean;
  timestamp?: number;
}

type AgentNode = "supervisor" | "search" | "rag" | "explain" | null;

const STARTER_TILES = [
  {
    icon: Database,
    title: "Vector Databases",
    query: "What are the best vector databases for RAG applications?",
    color: "#0D7377",
    borderColor: "border-[#0D7377]/30",
    bgColor: "bg-[#0D7377]/5",
    iconColor: "text-[#0D7377]",
  },
  {
    icon: Layers,
    title: "RAG Frameworks",
    query: "Compare LangChain vs LlamaIndex for building RAG",
    color: "#14B8A6",
    borderColor: "border-[#14B8A6]/30",
    bgColor: "bg-[#14B8A6]/5",
    iconColor: "text-[#14B8A6]",
  },
  {
    icon: Workflow,
    title: "Agent Frameworks",
    query: "What frameworks are best for building AI agents?",
    color: "#A78BFA",
    borderColor: "border-[#A78BFA]/30",
    bgColor: "bg-[#A78BFA]/5",
    iconColor: "text-[#A78BFA]",
  },
  {
    icon: Network,
    title: "MCP Servers",
    query: "What are Model Context Protocol servers and which ones are popular?",
    color: "#FF6B6B",
    borderColor: "border-[#FF6B6B]/30",
    bgColor: "bg-[#FF6B6B]/5",
    iconColor: "text-[#FF6B6B]",
  },
];

function TypingIndicator() {
  return (
    <div className="flex items-center gap-1 py-1">
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          className="w-1.5 h-1.5 rounded-full bg-white/40"
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{ repeat: Infinity, duration: 1, delay: i * 0.2 }}
        />
      ))}
    </div>
  );
}

function AgentBadge({ agent }: { agent: AgentNode }) {
  const labels: Record<string, { label: string; color: string }> = {
    supervisor: { label: "Routing request", color: "text-[#14B8A6]" },
    search: { label: "Searching the web", color: "text-[#0D7377]" },
    rag: { label: "Retrieving tools", color: "text-[#A78BFA]" },
    explain: { label: "Generating response", color: "text-[#14B8A6]" },
  };
  
  if (!agent || !labels[agent]) return null;
  const { label, color } = labels[agent];
  
  return (
    <motion.span
      initial={{ opacity: 0, x: 10 }}
      animate={{ opacity: 1, x: 0 }}
      className={`flex items-center gap-1.5 text-sm ${color}`}
    >
      <Loader2 className="w-3.5 h-3.5 animate-spin" />
      <span className="font-medium">Agent: {label}</span>
    </motion.span>
  );
}

function AskPageContent() {
  const searchParams = useSearchParams();
  const [query, setQuery] = useState(searchParams.get("q") || "");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentAgent, setCurrentAgent] = useState<AgentNode>(null);
  const [autoScroll, setAutoScroll] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const abortRef = useRef<AbortController | null>(null);
  const isMountedRef = useRef(true);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (autoScroll) {
      scrollToBottom();
    }
  }, [messages, autoScroll]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    return () => {
      isMountedRef.current = false;
      abortRef.current?.abort();
    };
  }, []);

  const handleScroll = useCallback(() => {
    const container = chatContainerRef.current;
    if (!container) return;

    const distanceFromBottom =
      container.scrollHeight - container.scrollTop - container.clientHeight;
    setAutoScroll(distanceFromBottom < 80);
  }, []);

  useEffect(() => {
    const initialQuery = searchParams.get("q");
    if (initialQuery && messages.length === 0 && !isLoading) {
      submitSearch(initialQuery);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams]);

  const submitSearch = useCallback(async (q: string) => {
    if (!q.trim() || isLoading) return;

    const userMsgId = Date.now().toString();
    setMessages((prev) => [
      ...prev,
      { id: userMsgId, role: "user", content: q, timestamp: Date.now() },
    ]);
    setQuery("");
    setIsLoading(true);
    setCurrentAgent("supervisor");
    setAutoScroll(true);

    const controller = new AbortController();
    abortRef.current = controller;

    const aiMsgId = (Date.now() + 1).toString();

    try {
      setMessages((prev) => [
        ...prev,
        { id: aiMsgId, role: "assistant", content: "", isStreaming: true, timestamp: Date.now() },
      ]);

      // Prepare conversation history (exclude current query)
      const conversationHistory = messages.map((msg) => ({
        role: msg.role,
        content: msg.content,
        timestamp: msg.timestamp,
      }));

      const response = await fetch(`${API_URL}/api/query/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: q,
          messages: conversationHistory,
        }),
        signal: controller.signal,
      });

      if (!response.ok) throw new Error(`Server returned ${response.status}`);
      if (!response.body) throw new Error("No data stream");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let finalResponse = "";
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        if (!isMountedRef.current || controller.signal.aborted) return;

        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;
        const lines = buffer.split("\n");
        buffer = lines.pop() ?? "";

        for (const line of lines) {
          if (!line.trim()) continue;
          if (line.startsWith("data: ")) {
            const data = line.slice(6);
            if (data === "[DONE]" || data.includes('"done": true')) continue;

            try {
              const parsed = JSON.parse(data);

              if (parsed.node) {
                const agentMap: Record<string, AgentNode> = {
                  supervisor: "supervisor",
                  search: "search",
                  rag: "rag",
                  explain: "explain",
                };
                if (agentMap[parsed.node] && isMountedRef.current) {
                  setCurrentAgent(agentMap[parsed.node]);
                }
              }

              if (parsed.final_response) {
                finalResponse = parsed.final_response;
                if (isMountedRef.current) {
                  setMessages((prev) =>
                    prev.map((msg) =>
                      msg.id === aiMsgId ? { ...msg, content: finalResponse } : msg
                    )
                  );
                }
              }
            } catch {
              // Skip parse errors
            }
          }
        }
      }

      if (isMountedRef.current) {
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === aiMsgId ? { ...msg, isStreaming: false } : msg
          )
        );
      }
    } catch (error) {
      if (controller.signal.aborted || !isMountedRef.current) {
        return;
      }

      const result = handleAPIError(error, () => submitSearch(q));

      if (result.shouldRetry) {
        setMessages((prev) => prev.filter((m) => m.content !== "" || m.role === "user"));
      }
    } finally {
      if (abortRef.current === controller) {
        abortRef.current = null;
      }

      if (isMountedRef.current) {
        setIsLoading(false);
        setCurrentAgent(null);
      }
    }
  }, [isLoading]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    submitSearch(query);
  };

  const handleStarterClick = (starterQuery: string) => {
    submitSearch(starterQuery);
  };

  const isEmpty = messages.length === 0;

  return (
    <div className="relative flex flex-col h-screen">
      {/* Subtle animated background */}
      <FloatingOrbs />

      {/* Header - fixed at top */}
      <header className="relative z-10 h-14 border-b border-white/[0.06] flex items-center justify-between px-4 shrink-0 bg-black/60 backdrop-blur-xl">
        <div className="flex items-center gap-3">
          <Link 
            href="/" 
            className="p-2 -ml-2 rounded-lg hover:bg-white/5 transition-colors"
          >
            <ArrowLeft className="w-5 h-5 text-white/50 hover:text-white/80 transition-colors" />
          </Link>
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#0D7377]/30 to-[#14B8A6]/20 flex items-center justify-center border border-[#0D7377]/30">
              <Hexagon className="w-4 h-4 text-[#14B8A6]" />
            </div>
            <span className="font-bold text-white tracking-tight">ToolChainDev</span>
          </div>
        </div>
        
        {isLoading && <AgentBadge agent={currentAgent} />}
      </header>

      {/* Chat Area - scrollable */}
      <div 
        ref={chatContainerRef}
        onScroll={handleScroll}
        className="relative z-10 flex-1 overflow-y-auto overscroll-contain"
        style={{ minHeight: 0 }}
      >
        <div className="max-w-3xl mx-auto px-4 py-6">
          {isEmpty ? (
            /* Empty State with Luxury Starter Tiles */
            <div className="flex flex-col items-center justify-center min-h-[60vh] py-12">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center mb-10"
              >
                {/* Premium icon with animated border glow */}
                <motion.div 
                  className="relative w-16 h-16 mx-auto mb-6"
                >
                  <motion.div
                    className="absolute inset-0 rounded-2xl"
                    style={{ 
                      border: '1px solid rgba(13, 115, 119, 0.4)',
                    }}
                    animate={{ 
                      borderColor: ['rgba(13, 115, 119, 0.3)', 'rgba(20, 184, 166, 0.6)', 'rgba(13, 115, 119, 0.3)']
                    }}
                    transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                  />
                  <div className="absolute inset-0 rounded-2xl bg-black/80 flex items-center justify-center border border-white/[0.08]">
                    <Hexagon className="w-7 h-7 text-[#14B8A6]" />
                  </div>
                </motion.div>
                
                <h1 className="text-2xl font-bold text-white mb-3">
                  What can I help you discover?
                </h1>
                <p className="text-white/50 text-sm max-w-md leading-relaxed">
                  Ask about AI tools, frameworks, vector databases, or anything in the AI ecosystem
                </p>
              </motion.div>

              {/* Luxury Black Glass Starter Tiles */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-2xl">
                {STARTER_TILES.map((tile, index) => (
                  <motion.button
                    key={tile.title}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    onClick={() => handleStarterClick(tile.query)}
                    whileHover={{ scale: 1.02, y: -2 }}
                    whileTap={{ scale: 0.98 }}
                    className="group relative p-5 text-left overflow-hidden"
                  >
                    {/* Black glass background */}
                    <div className="absolute inset-0 bg-black/80 rounded-xl" />
                    
                    {/* Subtle color wash */}
                    <div 
                      className="absolute inset-0 rounded-xl opacity-10"
                      style={{ 
                        background: `radial-gradient(ellipse at 30% 30%, ${tile.color}40, transparent 70%)`
                      }}
                    />
                    
                    {/* Border with hover glow */}
                    <div className={`absolute inset-0 rounded-xl border ${tile.borderColor} group-hover:border-opacity-60 transition-all`} />
                    <motion.div 
                      className="absolute inset-0 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                      style={{ 
                        boxShadow: `0 0 20px ${tile.color}25, inset 0 0 20px ${tile.color}10`
                      }}
                    />
                    
                    {/* Content */}
                    <div className="relative">
                      <div 
                        className="w-10 h-10 rounded-lg flex items-center justify-center mb-3 border transition-all duration-300"
                        style={{ 
                          background: `${tile.color}10`,
                          borderColor: `${tile.color}30`
                        }}
                      >
                        <tile.icon 
                          className="w-5 h-5 transition-all duration-300"
                          style={{ color: tile.color }}
                        />
                      </div>
                      <h3 className="font-semibold text-white mb-1.5 group-hover:text-white transition-colors">
                        {tile.title}
                      </h3>
                      <p className="text-xs text-white/40 line-clamp-2 leading-relaxed group-hover:text-white/55 transition-colors">
                        {tile.query}
                      </p>
                    </div>
                  </motion.button>
                ))}
              </div>
            </div>
          ) : (
            /* Message Thread */
            <div className="space-y-5 pb-36">
              <AnimatePresence initial={false}>
                {messages.map((msg) => {
                  const isUser = msg.role === "user";
                  const timestamp = msg.timestamp
                    ? new Date(msg.timestamp).toLocaleTimeString('en-US', {
                        hour: 'numeric',
                        minute: '2-digit',
                      })
                    : '';

                  return (
                    <motion.div
                      key={msg.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.2 }}
                      className={`flex gap-4 ${isUser ? "justify-end" : "justify-start"} mb-6`}
                    >
                      {/* AI Avatar - Holographic style */}
                      {!isUser && (
                        <motion.div 
                          className="w-8 h-8 rounded-full bg-[#0D7377]/30 flex items-center justify-center shrink-0 border border-[#14B8A6]/40"
                          animate={{ 
                            boxShadow: ['0 0 10px rgba(20, 184, 166, 0.2)', '0 0 20px rgba(20, 184, 166, 0.4)', '0 0 10px rgba(20, 184, 166, 0.2)']
                          }}
                          transition={{ duration: 2, repeat: Infinity }}
                        >
                          <Hexagon className="w-4 h-4 text-[#14B8A6]" />
                        </motion.div>
                      )}

                      {/* Message Card - Holographic for AI */}
                      <div
                        className={`relative max-w-[85%] overflow-hidden ${
                          isUser
                            ? "bg-white/5 border border-white/10 rounded-xl"
                            : "bg-black/60 border border-[#0D7377]/30 rounded-xl"
                        } p-4 shadow-lg`}
                        style={!isUser ? { 
                          boxShadow: '0 0 20px rgba(13, 115, 119, 0.15), inset 0 0 30px rgba(20, 184, 166, 0.03)'
                        } : undefined}
                      >
                        {/* Holographic scan lines overlay - AI only */}
                        {!isUser && (
                          <>
                            <div 
                              className="absolute inset-0 pointer-events-none opacity-[0.03]"
                              style={{
                                backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(20, 184, 166, 0.5) 2px, rgba(20, 184, 166, 0.5) 3px)',
                              }}
                            />
                            <motion.div 
                              className="absolute inset-0 pointer-events-none"
                              style={{
                                background: 'linear-gradient(180deg, rgba(20, 184, 166, 0.05) 0%, transparent 10%, transparent 90%, rgba(20, 184, 166, 0.05) 100%)'
                              }}
                              animate={{ opacity: [0.5, 0.8, 0.5] }}
                              transition={{ duration: 3, repeat: Infinity }}
                            />
                          </>
                        )}
                        
                        {/* Header: Role + Timestamp */}
                        <div className={`relative flex items-center justify-between mb-2 pb-2 border-b ${isUser ? 'border-white/10' : 'border-[#14B8A6]/20'}`}>
                          <span className={`text-xs font-medium uppercase tracking-wide ${isUser ? 'text-white/60' : 'text-[#14B8A6]'}`}>
                            {isUser ? "You" : "ToolChainDev AI"}
                          </span>
                          {timestamp && (
                            <span className="text-xs text-white/40 font-mono">{timestamp}</span>
                          )}
                        </div>

                        {/* Message Content */}
                        <div className="relative">
                          {isUser ? (
                            <p className="text-white/90 leading-relaxed">{msg.content}</p>
                          ) : (
                            msg.content ? (
                              <div className="prose-ai-response">
                                <ReactMarkdown
                                  remarkPlugins={[remarkGfm]}
                                  components={{
                                    table: ({ children, ...props }) => (
                                      <div className="my-3 overflow-x-auto">
                                        <table className="w-full border-collapse" {...props}>
                                          {children}
                                        </table>
                                      </div>
                                    ),
                                    th: ({ children, ...props }) => (
                                      <th
                                        className="border-b border-[#14B8A6]/30 px-3 py-2 text-left text-xs font-semibold text-white/80"
                                        {...props}
                                      >
                                        {children}
                                      </th>
                                    ),
                                    td: ({ children, ...props }) => (
                                      <td
                                        className="border-b border-[#14B8A6]/15 px-3 py-2 align-top text-xs text-white/70"
                                        {...props}
                                      >
                                        {children}
                                      </td>
                                    ),
                                  }}
                                >
                                  {msg.content}
                                </ReactMarkdown>
                              </div>
                            ) : (
                              <TypingIndicator />
                            )
                          )}
                        </div>

                        {/* Agent Status (for AI messages with streaming) */}
                        {!isUser && msg.isStreaming && (
                          <div className="mt-3 pt-3 border-t border-[#14B8A6]/20">
                            <div className="flex items-center gap-2 text-xs text-[#14B8A6]">
                              <Loader2 className="w-3 h-3 animate-spin" />
                              <span className="font-mono">Thinking...</span>
                            </div>
                          </div>
                        )}
                      </div>

                      {/* User Avatar (right side) */}
                      {isUser && (
                        <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center shrink-0">
                          <User className="w-4 h-4 text-white/60" />
                        </div>
                      )}
                    </motion.div>
                  );
                })}
              </AnimatePresence>
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      {/* Input Area - fixed at bottom */}
      <div className="relative z-10 shrink-0 bg-gradient-to-t from-black/80 via-black/60 to-transparent pt-6 pb-6 px-4">
        <div className="max-w-3xl mx-auto">
          <form onSubmit={handleSearch} className="relative">
            <div className="flex items-center bg-black/60 border border-white/[0.08] rounded-xl overflow-hidden focus-within:border-[#0D7377]/40 focus-within:bg-black/80 transition-all shadow-lg shadow-black/30">
              <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask about AI tools..."
                className="flex-1 bg-transparent h-12 px-4 text-white placeholder:text-white/30 focus:outline-none text-sm"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !query.trim()}
                className="h-9 w-9 mr-1.5 rounded-lg bg-[#14B8A6] hover:bg-[#14B8A6]/80 text-black flex items-center justify-center transition-all disabled:opacity-30 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Send className="w-4 h-4" />
                )}
              </button>
            </div>
          </form>
          <p className="text-center text-[11px] text-white/25 mt-2.5">
            AI may produce inaccurate information. Verify important details.
          </p>
        </div>
      </div>
    </div>
  );
}

export default function AskPage() {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center h-screen bg-[#0a0a0f]">
          <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
        </div>
      }
    >
      <AskPageContent />
    </Suspense>
  );
}
