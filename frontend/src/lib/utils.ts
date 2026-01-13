import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import { env } from "./env";

export const API_URL = env.NEXT_PUBLIC_API_URL;

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatCategory(category: string): string {
  if (!category) return "";
  const map: Record<string, string> = {
    api: "API",
    mcp: "MCP Server",
    sdk: "SDK",
    framework: "Framework",
    model: "Model",
    vector_db: "Vector DB",
    agent_framework: "Agent Framework",
    cli: "CLI Tool",
    observability: "Observability",
    deployment: "Deployment",
  };
  return map[category] || category.charAt(0).toUpperCase() + category.slice(1).replace(/_/g, " ");
}

export function formatPricing(pricing: string): string {
  if (!pricing) return "";
  const map: Record<string, string> = {
    free: "Free",
    freemium: "Freemium",
    paid: "Paid",
    enterprise: "Enterprise",
  };
  return map[pricing.toLowerCase()] || pricing;
}
