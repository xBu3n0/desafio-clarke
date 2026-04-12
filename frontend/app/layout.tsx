import type { Metadata } from "next";
import { cookies } from "next/headers";
import { Roboto } from "next/font/google";

import { AppFooter } from "@/components/layout/AppFooter";
import { AppNavbar } from "@/components/layout/AppNavbar";

import "./globals.css";

const roboto = Roboto({
  variable: "--font-roboto",
  weight: ["400", "500", "700"],
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Clarke Energia | Comparador",
  description: "Comparador minimalista de fornecedores e soluções por estado.",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const cookieStore = await cookies();
  const cookieTheme = cookieStore.get("clarke_theme")?.value;
  const initialTheme = cookieTheme === "dark" ? "dark" : "light";

  return (
    <html
      lang="en"
      suppressHydrationWarning
      data-theme={initialTheme}
      className={`${roboto.variable} ${initialTheme === "dark" ? "theme-dark" : "theme-light"} h-full antialiased`}
    >
      <body className="m-0 flex min-h-full flex-col bg-(--bg) font-sans text-(--text)">
        <AppNavbar />
        {children}
        <AppFooter />
      </body>
    </html>
  );
}
