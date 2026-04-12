import * as React from "react";

import { cn } from "@/lib/utils";

export type SelectProps = React.SelectHTMLAttributes<HTMLSelectElement> & {
  hasError?: boolean;
};

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, hasError = false, ...props }, ref) => {
    return (
      <select
        ref={ref}
        className={cn(
          "min-h-11 border border-(--line) bg-(--panel) px-3 py-2 text-(--text) transition",
          hasError &&
            "border-(--danger-line) ring-2 ring-(--danger-soft) focus:border-(--danger-line) focus:ring-2 focus:ring-(--danger-soft)",
          className,
        )}
        {...props}
      />
    );
  },
);

Select.displayName = "Select";
