import * as React from "react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback?: React.ReactNode },
  State
> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("ErrorBoundary caught:", error, errorInfo);
  }

  render() {
    if (this.state.hasError && this.state.error) {
      if (this.props.fallback) return this.props.fallback;
      return (
        <Card padding="lg" className="mx-auto max-w-md text-center">
          <h2 className="text-lg font-semibold text-slate-800">Something went wrong</h2>
          <p className="mt-2 text-sm text-slate-600">{this.state.error.message}</p>
          <Button
            variant="primary"
            className="mt-4"
            onClick={() => this.setState({ hasError: false, error: null })}
          >
            Try again
          </Button>
        </Card>
      );
    }
    return this.props.children;
  }
}
