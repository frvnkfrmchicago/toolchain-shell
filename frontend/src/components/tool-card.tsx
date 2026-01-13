"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ExternalLink, Github } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { formatCategory, formatPricing } from "@/lib/utils";
import type { AITool } from "@/types";

interface ToolCardProps {
  tool: AITool;
  index?: number;
}

const pricingColors: Record<string, "success" | "default" | "secondary" | "destructive"> = {
  free: "success",
  freemium: "default",
  paid: "secondary",
  enterprise: "destructive",
};

export function ToolCard({ tool, index = 0 }: ToolCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.3,
        delay: index * 0.05,
        ease: [0.4, 0, 0.2, 1],
      }}
    >
      <Link href={`/tools/${tool.id}`}>
        <Card className="h-full cursor-pointer group">
          <CardHeader className="pb-3">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <CardTitle className="text-lg group-hover:text-primary transition-colors">
                  {tool.name}
                </CardTitle>
                <p className="text-sm text-muted-foreground mt-1">
                  {tool.provider}
                </p>
              </div>
              <Badge variant={pricingColors[tool.pricing] || "default"}>
                {formatPricing(tool.pricing)}
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            {/* Category badge */}
            <div className="flex flex-wrap gap-2 mb-3">
              <Badge variant="outline" className="text-xs">
                {formatCategory(tool.category)}
              </Badge>
              <Badge variant="muted" className="text-xs">
                {tool.subcategory}
              </Badge>
            </div>

            {/* Description */}
            <p className="text-sm text-muted-foreground line-clamp-2 mb-4">
              {tool.description}
            </p>

            {/* Languages */}
            <div className="flex flex-wrap gap-1 mb-4">
              {tool.languages.slice(0, 4).map((lang) => (
                <span
                  key={lang}
                  className="text-xs px-2 py-0.5 rounded bg-muted text-muted-foreground"
                >
                  {lang}
                </span>
              ))}
              {tool.languages.length > 4 && (
                <span className="text-xs px-2 py-0.5 rounded bg-muted text-muted-foreground">
                  +{tool.languages.length - 4}
                </span>
              )}
            </div>

            {/* Links */}
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <span className="flex items-center gap-1 hover:text-foreground transition-colors">
                <ExternalLink className="w-3 h-3" />
                Docs
              </span>
              {tool.github_url && (
                <span className="flex items-center gap-1 hover:text-foreground transition-colors">
                  <Github className="w-3 h-3" />
                  GitHub
                </span>
              )}
            </div>
          </CardContent>
        </Card>
      </Link>
    </motion.div>
  );
}
