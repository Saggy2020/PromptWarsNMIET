import type { Metadata } from 'next';
import './globals.css';
import { Navbar } from '../components/Navbar';
import { DemoBanner } from '../components/DemoBanner';
import { AssistantDrawer } from '../components/AssistantDrawer';

export const metadata: Metadata = {
  title: 'PantryPilot: Autonomous Food-Intelligence & Safety System',
  description: 'Multi-agent household food waste reduction enforcing deterministic dietary & medical constraints.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-slate-50 text-slate-900 antialiased">
        <DemoBanner />
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {children}
        </main>
        <AssistantDrawer />
        <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
          <p>PantryPilot: Built for Hackathon 'Build Beyond AI: Engineer Secure, Intelligent & Autonomous Applications'</p>
          <p className="mt-1">Powered by Google Cloud Run, Vertex AI Gemini, and Deterministic Safety Guardian.</p>
        </footer>
      </body>
    </html>
  );
}
