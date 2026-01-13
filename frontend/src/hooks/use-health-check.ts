"use client";

/**
 * useHealthCheck - Monitor backend API health status
 *
 * Per skills-library-v2/agents/deployment/SKILL.md:
 * - Periodic health checks to backend
 * - Surface connection status to UI
 */

import { useState, useEffect, useCallback } from "react";
import { API_URL } from "@/lib/utils";

interface HealthStatus {
  isHealthy: boolean | null;
  lastChecked: Date | null;
  error: string | null;
  version: string | null;
}

export function useHealthCheck(intervalMs = 30000): HealthStatus {
  const [status, setStatus] = useState<HealthStatus>({
    isHealthy: null,
    lastChecked: null,
    error: null,
    version: null,
  });

  const checkHealth = useCallback(async () => {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);

      const response = await fetch(`${API_URL}/health`, {
        method: "GET",
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (response.ok) {
        const data = await response.json();
        setStatus({
          isHealthy: true,
          lastChecked: new Date(),
          error: null,
          version: data.version || null,
        });
      } else {
        setStatus({
          isHealthy: false,
          lastChecked: new Date(),
          error: `Server returned ${response.status}`,
          version: null,
        });
      }
    } catch (err) {
      setStatus({
        isHealthy: false,
        lastChecked: new Date(),
        error:
          err instanceof Error
            ? err.name === "AbortError"
              ? "Request timed out"
              : err.message
            : "Unknown error",
        version: null,
      });
    }
  }, []);

  useEffect(() => {
    // Initial check
    checkHealth();

    // Set up interval
    const interval = setInterval(checkHealth, intervalMs);

    return () => clearInterval(interval);
  }, [checkHealth, intervalMs]);

  return status;
}
