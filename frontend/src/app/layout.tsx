import type { Metadata } from "next";
import { Inter, Space_Grotesk, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "sonner";
import { SmoothScroll } from "@/components/providers/smooth-scroll";
import { OfflineBanner } from "@/components/offline-banner";

const inter = Inter({
  variable: "--font-body",
  subsets: ["latin"],
  display: "swap",
});

const spaceGrotesk = Space_Grotesk({
  variable: "--font-heading",
  subsets: ["latin"],
  display: "swap",
  weight: ["400", "500", "600", "700"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "ToolChainDev - AI Tool Discovery Platform",
  description: "Discover AI development tools, APIs, MCPs, SDKs, and frameworks. Ask questions and get AI-powered recommendations.",
  keywords: ["AI tools", "LangChain", "Vector DB", "MCP", "LLM", "RAG", "AI development"],
  openGraph: {
    title: "ToolChainDev - AI Tool Discovery Platform",
    description: "Discover AI development tools and get AI-powered recommendations",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${inter.variable} ${spaceGrotesk.variable} ${jetbrainsMono.variable} antialiased selection:bg-primary selection:text-black`}
        suppressHydrationWarning
      >
        <OfflineBanner />
        <SmoothScroll>
          {children}
        </SmoothScroll>
        <Toaster
          position="bottom-right"
          theme="dark"
          toastOptions={{
            style: {
              background: "#0A0A0F",
              border: "1px solid rgba(255,255,255,0.1)",
              color: "#fff",
            },
          }}
        />
      </body>
    </html>
  );
}
