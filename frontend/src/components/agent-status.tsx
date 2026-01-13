"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface AgentStatusProps {
  currentAgent: string | null;
  isProcessing: boolean;
  className?: string;
}

const agentColors: Record<string, string> = {
  supervisor: "from-purple-500 to-blue-500",
  search: "from-blue-500 to-cyan-500",
  rag: "from-green-500 to-emerald-500",
  explain: "from-orange-500 to-yellow-500",
};

const agentLabels: Record<string, string> = {
  supervisor: "Routing",
  search: "Searching Web",
  rag: "Retrieving Tools",
  explain: "Generating Response",
};

export function AgentStatus({ currentAgent, isProcessing, className }: AgentStatusProps) {
  if (!isProcessing && !currentAgent) {
    return null;
  }

  const gradientClass = currentAgent ? agentColors[currentAgent] || "from-gray-500 to-gray-600" : "from-gray-500 to-gray-600";
  const label = currentAgent ? agentLabels[currentAgent] || currentAgent : "Processing";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className={cn("flex items-center gap-3", className)}
    >
      {/* Animated orb */}
      <div className="relative">
        <motion.div
          className={cn(
            "w-3 h-3 rounded-full bg-gradient-to-r",
            gradientClass
          )}
          animate={{
            scale: [1, 1.2, 1],
            opacity: [1, 0.8, 1],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        {/* Glow effect */}
        <motion.div
          className={cn(
            "absolute inset-0 rounded-full bg-gradient-to-r blur-md",
            gradientClass
          )}
          animate={{
            scale: [1, 1.5, 1],
            opacity: [0.5, 0.2, 0.5],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>

      {/* Label */}
      <span className="text-sm text-muted-foreground">
        {label}
        <motion.span
          animate={{ opacity: [1, 0.3, 1] }}
          transition={{ duration: 1, repeat: Infinity }}
        >
          ...
        </motion.span>
      </span>
    </motion.div>
  );
}
