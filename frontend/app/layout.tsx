import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'ReplySight - Research-Backed Customer Service',
  description: 'Generate empathetic, research-backed customer service responses with citations',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
} 