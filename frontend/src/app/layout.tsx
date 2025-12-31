import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "REFY AI - Analyse de faisabilité immobilière",
  description: "Outil B2B d'automatisation de l'étude de faisabilité immobilière",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
