import type { Metadata } from "next";
import { Geist, Geist_Mono, Source_Code_Pro, Source_Sans_3 } from "next/font/google";
import "./globals.css";

const scpSans = Source_Sans_3({
  variable: "--font-source-sans-3",
  subsets: ["latin"],
});

const scpMono = Source_Code_Pro({
  variable: "--font-source-code-pro",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Claudemob",
  description: "Claudes mob to find god",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${scpSans.variable} ${scpMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
