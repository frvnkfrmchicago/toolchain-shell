/**
 * Type definitions for ToolChainDev API
 */

export interface AITool {
  id: string;
  name: string;
  category: "api" | "mcp" | "sdk" | "cli" | "vector_db" | "framework" | "agent_framework";
  subcategory: string;
  description: string;
  provider: string;
  pricing: "free" | "freemium" | "paid" | "enterprise";
  languages: string[];
  use_cases: string[];
  documentation_url: string;
  github_url: string | null;
  npm_package: string | null;
  pypi_package: string | null;
  code_example: string;
  pros: string[];
  cons: string[];
  alternatives: string[];
  popularity_score: number;
}

export interface Category {
  id: string;
  name: string;
  count: number;
}

export interface QueryResponse {
  query: string;
  response: string;
  messages: string[];
}

export interface StreamEvent {
  node?: string;
  messages?: string[];
  final_response?: string;
  done?: boolean;
}
