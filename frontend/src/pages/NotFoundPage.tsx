import { useTranslation } from "react-i18next";
import { Link, useNavigate } from "react-router-dom";
import { Home, ArrowLeft, Search } from "lucide-react";
import { Button } from "@/components/ui/Button";

export function NotFoundPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 bg-stone-50 dark:bg-stone-950">
      <div className="text-center max-w-md">
        <div className="relative mb-8">
          <h1 className="text-9xl font-bold text-stone-200 dark:text-stone-800 select-none">
            404
          </h1>
          <div className="absolute inset-0 flex items-center justify-center">
            <Search className="h-16 w-16 text-teal-600 dark:text-teal-400" />
          </div>
        </div>
        <h2 className="text-2xl font-semibold text-stone-900 dark:text-stone-100 mb-4">
          {t("notFound.title", "Page Not Found")}
        </h2>
        <p className="text-stone-600 dark:text-stone-400 mb-8">
          {t("notFound.description", "The page you're looking for doesn't exist or has been moved.")}
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Button asChild>
            <Link to="/"><Home className="h-4 w-4 mr-2" />{t("notFound.goHome", "Go Home")}</Link>
          </Button>
          <Button variant="outline" onClick={() => navigate(-1)}>
            <ArrowLeft className="h-4 w-4 mr-2" />{t("notFound.goBack", "Go Back")}
          </Button>
        </div>
      </div>
    </div>
  );
}
