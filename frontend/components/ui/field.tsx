import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

type FieldProps = {
  label: string;
  error?: string;
  children: ReactNode;
  className?: string;
};

export function Field({ label, error, children, className }: FieldProps) {
  const hasError = Boolean(error);

  return (
    <label className={cn("grid gap-1.5", className)}>
      <span className="text-xs tracking-wide text-(--muted) uppercase">{label}</span>
      {children}
      <p
        className={cn(
          "mt-1 mb-0 min-h-4 text-xs",
          hasError ? "text-(--danger)" : "invisible",
        )}
        aria-live={hasError ? "polite" : undefined}
      >
        {error ?? "\u00A0"}
      </p>
    </label>
  );
}
