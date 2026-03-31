import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    // Performance optimizations
    target: "esnext",
    minify: "terser",
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
    rollupOptions: {
      output: {
        // Code splitting for better caching
        manualChunks: {
          // React core
          "react-vendor": ["react", "react-dom", "react-router-dom"],
          // UI components
          "ui-vendor": ["@radix-ui/react-select", "@radix-ui/react-tabs", "@radix-ui/react-dialog"],
          // Charts
          "chart-vendor": ["recharts"],
          // Syntax highlighting
          "syntax-vendor": ["react-syntax-highlighter"],
          // State management
          "state-vendor": ["zustand", "@tanstack/react-query"],
        },
        // Asset naming for better caching
        entryFileNames: "assets/[name]-[hash].js",
        chunkFileNames: "assets/[name]-[hash].js",
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split(".");
          const ext = info[info.length - 1];
          if (/\.(png|jpe?g|gif|svg|webp|ico)$/i.test(assetInfo.name)) {
            return "assets/images/[name]-[hash][extname]";
          }
          if (/\.(css)$/i.test(assetInfo.name)) {
            return "assets/styles/[name]-[hash][extname]";
          }
          return "assets/[name]-[hash][extname]";
        },
      },
    },
    // Optimize chunk size
    chunkSizeWarningLimit: 1000,
    // Source maps for debugging
    sourcemap: false,
    // CSS optimization
    cssCodeSplit: true,
    // Asset optimization
    assetsInlineLimit: 4096,
  },
  server: {
    port: 3000,
    open: true,
    hmr: {
      overlay: false,
    },
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
  // Preview server
  preview: {
    port: 3000,
  },
  // CSS optimization
  css: {
    devSourcemap: true,
  },
  // Dependency optimization
  optimizeDeps: {
    include: [
      "react",
      "react-dom",
      "react-router-dom",
      "zustand",
      "@tanstack/react-query",
      "recharts",
      "lucide-react",
      "framer-motion",
    ],
  },
});
