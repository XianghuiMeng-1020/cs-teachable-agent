import * as Dialog from "@radix-ui/react-dialog";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { useAppStore } from "@/stores/appStore";
import { createTA } from "@/api/client";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Code, Database, Brain, Sparkles, CheckCircle, ArrowRight } from "lucide-react";
import { useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

const DOMAIN_BASE = [
  {
    id: "python" as const,
    icon: Code,
    color: "bg-blue-500",
    lightColor: "bg-blue-50",
    textColor: "text-blue-600",
  },
  {
    id: "database" as const,
    icon: Database,
    color: "bg-emerald-500",
    lightColor: "bg-emerald-50",
    textColor: "text-emerald-600",
  },
  {
    id: "ai_literacy" as const,
    icon: Brain,
    color: "bg-violet-500",
    lightColor: "bg-violet-50",
    textColor: "text-violet-600",
  },
] as const;

interface DomainSelectorProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onComplete?: () => void;
}

export function DomainSelector({ open, onOpenChange, onComplete }: DomainSelectorProps) {
  const { t } = useTranslation();
  const domains = useMemo(
    () =>
      DOMAIN_BASE.map((d) => {
        if (d.id === "python") {
          return {
            ...d,
            label: t("onboarding.pythonLabel"),
            shortLabel: t("onboarding.pythonShort"),
            description: t("onboarding.pythonDesc"),
            features: t("onboarding.pythonFeatures", { returnObjects: true }) as string[],
            estimatedTime: t("onboarding.pythonTime"),
          };
        }
        if (d.id === "database") {
          return {
            ...d,
            label: t("onboarding.sqlLabel"),
            shortLabel: t("onboarding.sqlShort"),
            description: t("onboarding.sqlDesc"),
            features: t("onboarding.sqlFeatures", { returnObjects: true }) as string[],
            estimatedTime: t("onboarding.sqlTime"),
          };
        }
        return {
          ...d,
          label: t("onboarding.aiLabel"),
          shortLabel: t("onboarding.aiShort"),
          description: t("onboarding.aiDesc"),
          features: t("onboarding.aiFeatures", { returnObjects: true }) as string[],
          estimatedTime: t("onboarding.aiTime"),
        };
      }),
    [t]
  );
  const queryClient = useQueryClient();
  const { setCurrentTaId } = useAppStore();
  const [selectedDomain, setSelectedDomain] = useState<string | null>(null);
  const [step, setStep] = useState<"select" | "creating" | "success">("select");

  const createTAMutation = useMutation({
    mutationFn: (domain_id: string) => createTA(domain_id),
    onSuccess: (created) => {
      queryClient.invalidateQueries({ queryKey: ["ta", "list"] });
      setCurrentTaId(created.id);
      setStep("success");
      const label = domains.find((d) => d.id === created.domain_id)?.shortLabel ?? "";
      toast.success(
        t("onboarding.toastTaReady", {
          defaultValue: "Your {{label}} Teachable Agent is ready!",
          label,
        })
      );
    },
    onError: (err: Error) => {
      toast.error(err?.message ?? t("onboarding.failedCreateTA"));
      setStep("select");
    },
  });

  const handleCreate = () => {
    if (!selectedDomain) return;
    setStep("creating");
    createTAMutation.mutate(selectedDomain);
  };

  const handleClose = () => {
    onOpenChange(false);
    onComplete?.();
  };

  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm" />
        <Dialog.Content className="fixed left-1/2 top-1/2 z-50 w-full max-w-4xl -translate-x-1/2 -translate-y-1/2 rounded-2xl border border-stone-200 bg-white p-0 shadow-2xl overflow-hidden">
          {step === "select" && (
            <div className="p-8">
              <div className="text-center mb-8">
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-brand-50 rounded-full text-brand-600 text-sm font-medium mb-4">
                  <Sparkles className="w-4 h-4" />
                  {t("onboarding.welcomeToArtsCs")}
                </div>
                <Dialog.Title className="text-2xl font-bold text-stone-900">
                  {t("onboarding.chooseDomain")}
                </Dialog.Title>
                <Dialog.Description className="mt-2 text-stone-500 max-w-lg mx-auto">
                  {t("onboarding.chooseDomainDesc")}
                </Dialog.Description>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {domains.map((domain) => {
                  const Icon = domain.icon;
                  const isSelected = selectedDomain === domain.id;
                  return (
                    <Card
                      key={domain.id}
                      padding="lg"
                      className={`
                        cursor-pointer transition-all duration-200 border-2
                        ${isSelected ? `border-brand-500 ${domain.lightColor}` : 'border-transparent hover:border-stone-200'}
                      `}
                      onClick={() => setSelectedDomain(domain.id)}
                    >
                      <div className="flex flex-col h-full">
                        <div className={`w-12 h-12 ${domain.lightColor} ${domain.textColor} rounded-xl flex items-center justify-center mb-4`}>
                          <Icon className="w-6 h-6" />
                        </div>
                        <h3 className="font-semibold text-stone-900 mb-1">{domain.label}</h3>
                        <p className="text-sm text-stone-500 mb-4 flex-1">{domain.description}</p>
                        <div className="space-y-2">
                          {domain.features.map((feature, idx) => (
                            <div key={idx} className="flex items-center gap-2 text-xs text-stone-600">
                              <CheckCircle className="w-3 h-3 text-stone-400" />
                              {feature}
                            </div>
                          ))}
                        </div>
                        <div className="mt-4 pt-4 border-t border-stone-100">
                          <span className="text-xs text-stone-400">
                            {t("onboarding.estTime", { time: domain.estimatedTime })}
                          </span>
                        </div>
                      </div>
                    </Card>
                  );
                })}
              </div>

              <div className="mt-8 flex justify-end gap-3">
                <Button
                  variant="primary"
                  size="lg"
                  disabled={!selectedDomain}
                  onClick={handleCreate}
                  icon={ArrowRight}
                >
                  {t("onboarding.createMyTA")}
                </Button>
              </div>
            </div>
          )}

          {step === "creating" && (
            <div className="p-12 text-center">
              <div className="relative w-16 h-16 mx-auto mb-6">
                <div className="absolute inset-0 rounded-full border-4 border-stone-100" />
                <div className="absolute inset-0 rounded-full border-4 border-brand-500 border-t-transparent animate-spin" />
              </div>
              <h3 className="text-xl font-semibold text-stone-900 mb-2">{t("onboarding.creatingTA")}</h3>
              <p className="text-stone-500">
                {t("onboarding.settingUp", {
                  domain: domains.find((d) => d.id === selectedDomain)?.label ?? "",
                })}
              </p>
            </div>
          )}

          {step === "success" && (
            <div className="p-12 text-center">
              <div className="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <CheckCircle className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold text-stone-900 mb-2">{t("onboarding.taReady")}</h3>
              <p className="text-stone-500 mb-6 max-w-md mx-auto">
                {t("onboarding.taReadyDesc", {
                  domain: domains.find((d) => d.id === selectedDomain)?.shortLabel ?? "",
                })}
              </p>
              <Button variant="primary" size="lg" onClick={handleClose} icon={ArrowRight}>
                {t("onboarding.startTeaching")}
              </Button>
            </div>
          )}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
