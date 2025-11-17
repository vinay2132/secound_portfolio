import { JetBrains_Mono } from "next/font/google";
import "./globals.css";
import TawkToChat from "@/components/TawkToChat";
import { GoogleTagManager } from '@next/third-parties/google'

// Components
import Header from "@/components/Header";
import ErrorBoundary from "@/components/ErrorBoundary";
import PageTransition from "@/components/PageTransition";
import StairTransition from "@/components/StairTransition";

const jetbrainsMono = JetBrains_Mono({ 
  subsets: ["latin"], 
  weight: ["100","200","300","400","500","600","700","800"],
  variable: '--font-jetbrainsMono',
  display: 'swap',
  preload: true
 });

export const metadata = {
  title: "Vinay | Data Analyst & Full-Stack Developer",
  description: "Data Analyst with 3+ years of experience turning complex datasets into actionable insights, plus full-stack development across finance, healthcare, and e-commerce.",
  keywords: ["Vinay", "Data Analyst", "Full Stack Developer", "SQL", "Python", "Tableau", "Power BI", "React", "Node.js", "Next.js"],
  authors: [{ name: "Vinay" }],
  creator: "Vinay",
  publisher: "Vinay",
  robots: "index, follow",
  icons: {
    icon: '/assets/favicon.ico',
    shortcut: '/assets/favicon.ico',
    apple: '/assets/apple-touch-icon.png',
    other: {
      rel: 'apple-touch-icon-precomposed',
      url: '/assets/apple-touch-icon.png',
    },
  },
  manifest: '/site.webmanifest',
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://vinay2132.github.io/my_portfolio/",
    title: "Vinay | Data Analyst & Full-Stack Developer",
    description: "Data Analyst with 3+ years of experience in SQL, Python, Excel, Tableau and Power BI, building dashboards and models that drive strategic decisions.",
    siteName: "Vinay Portfolio",
    images: [
      {
        url: '/assets/Portfolio-picture.png',
        width: 1200,
        height: 630,
        alt: 'Vinay Portfolio Preview'
      }
    ]
  },
  twitter: {
    card: "summary_large_image",
    title: "Vinay | Data Analyst & Full-Stack Developer",
    description: "Data Analyst and full-stack developer working across finance, healthcare, and e-commerce.",
    creator: "@vinay",
    images: ['/assets/Portfolio-picture.png']
  },
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
    userScalable: false
  },
  themeColor: '#000000',
  colorScheme: 'dark',
  verification: {
    google: 'your-google-site-verification',
  },
  alternates: {
    canonical: 'https://vinay2132.github.io/my_portfolio/'
  }
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
        <meta name="theme-color" content="#000000" />
        <meta name="color-scheme" content="dark" />
        <link rel="icon" href="/assets/favicon.ico" sizes="any" />
        <link rel="icon" href="/assets/favicon-16x16.png" type="image/png" sizes="16x16" />
        <link rel="icon" href="/assets/favicon-32x32.png" type="image/png" sizes="32x32" />
        <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
        <link rel="manifest" href="/site.webmanifest" />
      </head>
      <GoogleTagManager gtmId="GTM-5727CZ8R" />
      <body className={jetbrainsMono.variable}>
        <ErrorBoundary>
          <Header />
          <StairTransition />
          <PageTransition>
            {children}
          </PageTransition>
        </ErrorBoundary>
        <TawkToChat />
      </body>
    </html>
  );
}
