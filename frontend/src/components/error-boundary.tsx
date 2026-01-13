"use client";

/**
 * ErrorBoundary - Catches React errors and displays fallback UI
 *
 * Per skills-library-v2/agents/error-handling/SKILL.md:
 * - Catch errors at component boundaries
 * - Show user-friendly fallback
 * - Allow recovery via retry
 */

import { Component, ReactNode } from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("ErrorBoundary caught error:", error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: undefined });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="flex flex-col items-center justify-center min-h-[50vh] p-8 text-center">
          <div className="w-16 h-16 rounded-full bg-red-500/10 flex items-center justify-center mb-6">
            <AlertTriangle className="w-8 h-8 text-red-400" />
          </div>

          <h2 className="text-xl font-bold text-white mb-2">Something went wrong</h2>

          <p className="text-white/50 text-sm max-w-md mb-6">
            {this.state.error?.message || "An unexpected error occurred"}
          </p>

          <button
            onClick={this.handleReset}
            className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Try again
          </button>

          {process.env.NODE_ENV === "development" && this.state.error && (
            <details className="mt-6 text-left w-full max-w-lg">
              <summary className="text-xs text-white/30 cursor-pointer hover:text-white/50">
                Technical details
              </summary>
              <pre className="mt-2 p-4 bg-white/5 rounded-lg text-xs text-red-400/80 overflow-auto">
                {this.state.error.stack}
              </pre>
            </details>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}
