import * as React from "react";

import { cn } from "@/lib/utils";

export function NavigationMenu({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLElement>) {
  return (
    <nav className={cn("max-w-full", className)} {...props}>
      {children}
    </nav>
  );
}

export function NavigationMenuList({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLUListElement>) {
  return (
    <ul className={cn("m-0 flex list-none gap-1 p-0", className)} {...props}>
      {children}
    </ul>
  );
}

export function NavigationMenuItem({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLLIElement>) {
  return (
    <li className={cn("m-0", className)} {...props}>
      {children}
    </li>
  );
}

type NavigationMenuLinkProps = React.AnchorHTMLAttributes<HTMLAnchorElement>;

export const NavigationMenuLink = React.forwardRef<HTMLAnchorElement, NavigationMenuLinkProps>(
  ({ className, children, ...props }, ref) => (
    <a
      ref={ref}
      className={cn(
        "inline-flex min-h-7 items-center gap-1 border border-(--line) bg-(--bg) px-2 py-1 text-xs text-(--text) no-underline transition hover:border-(--accent) hover:text-(--accent)",
        className,
      )}
      {...props}
    >
      {children}
    </a>
  ),
);

NavigationMenuLink.displayName = "NavigationMenuLink";
