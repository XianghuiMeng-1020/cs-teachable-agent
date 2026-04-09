import * as React from "react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { useTranslation } from "react-i18next";

interface State {
  hasError: boolean;
  error: Error | null;
  isChunkError: boolean;
}

// M-41: Check if error is a chunk load error
function isChunkLoadError(error: Error | null): boolean {
  if (!error) return false;
  const message = error.message.toLowerCase();
  return (
    message.includes("loading chunk") ||
    message.includes("chunk load") ||
    message.includes("failed to load dynamically imported module") ||
    message.includes("dynamic import")
  );
}

// M-41: Enhanced ErrorBoundary with chunk error support
export class ErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback?: React.ReactNode },
  State
> {
  state: State = { hasError: false, error: null, isChunkError: false };

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      isChunkError: isChunkLoadError(error),
    };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("ErrorBoundary caught:", error, errorInfo);
  }

  private handleRetry = () => {
    // M-41: For chunk errors, reload the page; otherwise reset state
    if (this.state.isChunkError) {
      window.location.reload();
    } else {
      this.setState({ hasError: false, error: null, isChunkError: false });
    }
  };

  render() {
    if (this.state.hasError && this.state.error) {
      if (this.props.fallback) return this.props.fallback;

      const { isChunkError } = this.state;
      const title = isChunkError
        ? "Failed to load page"
        : "Something went wrong";
      const message = isChunkError
        ? "The page couldn't be loaded. This might be due to a network issue or a new deployment."
        : this.state.error.message;
      const actionLabel = isChunkError ? "Reload page" : "Try again";

      return (
        <Card padding="lg" className="mx-auto max-w-md text-center">
          <h2 className="text-lg font-semibold text-stone-800">{title}</h2>
          <p className="mt-2 text-sm text-stone-600">{message}</p>
          <Button
            variant="primary"
            className="mt-4"
            onClick={this.handleRetry}
          >
            {actionLabel}
          </Button>
        </Card>
      );
    }
    return this.props.children;
  }
}

// M-41: AsyncErrorBoundary wrapper for lazy-loaded chunks with automatic retry
interface AsyncErrorBoundaryProps {
  children: React.ReactNode;
  maxRetries?: number;
}

interface AsyncErrorBoundaryState {
  hasError: boolean;
  retryCount: number;
}

export class AsyncErrorBoundary extends React.Component<
  AsyncErrorBoundaryProps,
  AsyncErrorBoundaryState
> {
  state: AsyncErrorBoundaryState = { hasError: false, retryCount: 0 };

  static getDerivedStateFromError(): AsyncErrorBoundaryState {
    return { hasError: true, retryCount: 0 };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("AsyncErrorBoundary caught chunk error:", error, errorInfo);
  }

  private handleRetry = () => {
    const { maxRetries = 3 } = this.props;
    const newCount = this.state.retryCount + 1;

    if (newCount <= maxRetries) {
      this.setState({ hasError: false, retryCount: newCount });
    } else {
      // Max retries reached, reload the page
      window.location.reload();
    }
  };

  render() {
    if (this.state.hasError) {
      const { maxRetries = 3 } = this.props;
      const remainingRetries = maxRetries - this.state.retryCount;

      return (
        <Card padding="lg" className="mx-auto max-w-md text-center">
          <h2 className="text-lg font-semibold text-stone-800">
            Failed to load page
          </h2>
          <p className="mt-2 text-sm text-stone-600">
            The page couldn't be loaded. This might be due to a network issue
            or a new deployment.
            {remainingRetries > 0 && (
              <span className="block mt-1">
                Retry {this.state.retryCount + 1} of {maxRetries}
              </span>
            )}
          </p>
          <div className="mt-4 flex gap-2 justify-center">
            <Button variant="primary" onClick={this.handleRetry}>
              {remainingRetries > 0 ? "Try again" : "Reload page"}
            </Button>
          </div>
        </Card>
      );
    }
    return this.props.children;
  }
}
