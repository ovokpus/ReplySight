/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  env: {
    API_BASE_URL: process.env.API_BASE_URL || 'http://localhost:8001',
  },
  async rewrites() {
    return [
      {
        source: '/api/respond',
        destination: '/api/respond',
      },
    ]
  },
}

module.exports = nextConfig 