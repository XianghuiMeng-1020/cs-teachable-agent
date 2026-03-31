import type { Metadata } from "next";
import { AppRouterCacheProvider } from "@mui/material-nextjs/v15-appRouter";
import type { CSSProperties } from "react";
import Providers from "./providers";
import "./globals.css";

export const metadata: Metadata = {
  title: "Assessment Studio",
  description: "AI-assistant assessment design workbench prototype built with Next.js and MUI."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body
        style={
          {
            "--font-display": '"Inter", "IBM Plex Sans", "Avenir Next", "Segoe UI", sans-serif',
            "--font-ui": '"Inter", "IBM Plex Sans", "Avenir Next", "Segoe UI", sans-serif',
            "--font-mono": '"IBM Plex Mono", "SFMono-Regular", Menlo, Monaco, monospace'
          } as CSSProperties
        }
      >
        <AppRouterCacheProvider options={{ enableCssLayer: true }}>
          <Providers>{children}</Providers>
        </AppRouterCacheProvider>
      </body>
    </html>
  );
}
