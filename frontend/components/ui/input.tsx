import * as React from "react";

import { cn } from "@/lib/utils";

export type InputProps = React.InputHTMLAttributes<HTMLInputElement> & {
  hasError?: boolean;
};

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, hasError = false, ...props }, ref) => {
    return (
      <input
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

Input.displayName = "Input";
