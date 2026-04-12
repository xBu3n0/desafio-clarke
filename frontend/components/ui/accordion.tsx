import * as React from "react";
import { ChevronDown } from "lucide-react";

import { cn } from "@/lib/utils";

type AccordionContextValue = {
  value: string | null;
  setValue: (next: string | null) => void;
  collapsible: boolean;
};

const AccordionContext = React.createContext<AccordionContextValue | null>(null);
const AccordionItemContext = React.createContext<{ value: string } | null>(null);

type AccordionProps = React.HTMLAttributes<HTMLDivElement> & {
  type?: "single";
  collapsible?: boolean;
  defaultValue?: string;
};

export function Accordion({
  className,
  collapsible = false,
  defaultValue,
  children,
  ...props
}: AccordionProps) {
  const [value, setValue] = React.useState<string | null>(defaultValue ?? null);

  return (
    <AccordionContext.Provider value={{ value, setValue, collapsible }}>
      <div className={cn("w-full", className)} {...props}>
        {children}
      </div>
    </AccordionContext.Provider>
  );
}

type AccordionItemProps = React.HTMLAttributes<HTMLDivElement> & {
  value: string;
};

export function AccordionItem({ className, value, children, ...props }: AccordionItemProps) {
  return (
    <AccordionItemContext.Provider value={{ value }}>
      <div className={cn("border border-(--line)", className)} {...props}>
        {children}
      </div>
    </AccordionItemContext.Provider>
  );
}

export function AccordionTrigger({
  className,
  children,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  const accordion = React.useContext(AccordionContext);
  const item = React.useContext(AccordionItemContext);

  if (!accordion || !item) {
    throw new Error("AccordionTrigger must be used inside AccordionItem.");
  }

  const isOpen = accordion.value === item.value;

  return (
    <button
      type="button"
      className={cn(
        "flex w-full items-center justify-between gap-2 px-4 py-3 text-left",
        className,
      )}
      aria-expanded={isOpen}
      onClick={() => {
        if (isOpen && accordion.collapsible) {
          accordion.setValue(null);
          return;
        }
        accordion.setValue(item.value);
      }}
      {...props}
    >
      <span>{children}</span>
      <ChevronDown
        size={16}
        className={cn("shrink-0 transition-transform", isOpen ? "rotate-180" : "rotate-0")}
        aria-hidden="true"
      />
    </button>
  );
}

export function AccordionContent({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  const accordion = React.useContext(AccordionContext);
  const item = React.useContext(AccordionItemContext);

  if (!accordion || !item) {
    throw new Error("AccordionContent must be used inside AccordionItem.");
  }

  const isOpen = accordion.value === item.value;

  return (
    <div
      className={cn(
        "grid transition-[grid-template-rows] duration-200",
        isOpen ? "grid-rows-[1fr]" : "grid-rows-[0fr]",
      )}
      aria-hidden={!isOpen}
      data-state={isOpen ? "open" : "closed"}
    >
      <div className="overflow-hidden">
        <div className={cn("px-4 pb-4", className)} {...props}>
          {children}
        </div>
      </div>
    </div>
  );
}
