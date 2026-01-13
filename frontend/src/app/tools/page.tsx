"use client";

import { Suspense } from "react";
import dynamic from "next/dynamic";

// Dynamic import to avoid SSR issues with useSearchParams
const ToolsContent = dynamic(() => import("./tools-content"), { ssr: false });

export default function ToolsPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-muted-foreground">Loading...</div>
      </div>
    }>
      <ToolsContent />
    </Suspense>
  );
}
