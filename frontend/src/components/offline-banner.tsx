"use client";

/**
 * OfflineBanner - Shows when backend is unreachable
 *
 * Per skills-library-v2/agents/deployment/SKILL.md:
 * - Display connection status to user
 * - Non-blocking but visible
 */

import { useHealthCheck } from "@/hooks/use-health-check";
import { AlertTriangle, RefreshCw } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function OfflineBanner() {
  const { isHealthy, error } = useHealthCheck(30000);

  // Don't show anything during initial check (null) or when healthy
  if (isHealthy !== false) {
    return null;
  }

  return (
    <AnimatePresence>
      <motion.div
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: -50, opacity: 0 }}
        className="fixed top-0 left-0 right-0 z-[100] bg-amber-500/90 backdrop-blur-sm text-black px-4 py-2"
      >
        <div className="max-w-4xl mx-auto flex items-center justify-center gap-3 text-sm font-medium">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>
            Backend is unreachable
            {error && <span className="opacity-70 ml-1">({error})</span>}
          </span>
          <button
            onClick={() => window.location.reload()}
            className="flex items-center gap-1 px-2 py-0.5 bg-black/10 hover:bg-black/20 rounded transition-colors"
          >
            <RefreshCw className="w-3 h-3" />
            Retry
          </button>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
