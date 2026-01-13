import { toast } from "sonner";
import { API_URL } from "./utils";

export interface APIErrorResult {
  message: string;
  isNetwork: boolean;
  shouldRetry: boolean;
}

export function handleAPIError(
  error: unknown,
  retry: () => void
): APIErrorResult {
  // Abort errors should be silent
  if (error instanceof Error && error.name === "AbortError") {
    return {
      message: "Request cancelled",
      isNetwork: false,
      shouldRetry: false,
    };
  }

  // Network errors (fetch failures)
  const isNetworkError =
    error instanceof TypeError && error.message.includes("fetch");

  const errorMessage = isNetworkError
    ? "Cannot connect to AI backend"
    : error instanceof Error
      ? error.message
      : "An unexpected error occurred";

  // Show toast notification
  toast.error(isNetworkError ? "Backend Offline" : "Request Failed", {
    description: errorMessage,
    action: {
      label: "Retry",
      onClick: retry,
    },
    duration: 10000,
  });

  return {
    message: errorMessage,
    isNetwork: isNetworkError,
    shouldRetry: true,
  };
}

export function isBackendReachable(apiUrl: string = API_URL): boolean {
  // Health check logic (optional utility)
  return true; // Placeholder
}
