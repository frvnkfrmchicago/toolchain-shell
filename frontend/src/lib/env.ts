/**
 * Environment Variable Validation
 *
 * Per skills-library-v2/agents/deployment/SKILL.md:
 * - Validate env vars at build time
 * - Fail fast with clear error messages
 * - Type-safe access throughout the app
 */

import { z } from "zod";

const envSchema = z.object({
  // Required: API URL for backend
  NEXT_PUBLIC_API_URL: z
    .string()
    .url("NEXT_PUBLIC_API_URL must be a valid URL")
    .default("http://localhost:8000"),
});

// Parse and validate environment variables
const parsed = envSchema.safeParse({
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
});

if (!parsed.success) {
  if (process.env.NODE_ENV !== 'production') {
    console.error(
      "❌ Invalid environment variables:",
      JSON.stringify(parsed.error.flatten().fieldErrors, null, 2)
    );
  }
  throw new Error("Invalid environment variables. Check .env.local file.");
}

export const env = parsed.data;

// Type for the validated env
export type Env = z.infer<typeof envSchema>;
