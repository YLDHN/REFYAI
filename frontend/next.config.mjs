/** @type {import('next').NextConfig} */
const nextConfig = {
  output: process.env.TAURI_ENV ? "export" : undefined,
  images: {
    unoptimized: process.env.TAURI_ENV ? true : false,
  },
  typescript: {
    ignoreBuildErrors: false,
  },
  eslint: {
    ignoreDuringBuilds: false,
  },
};

export default nextConfig;
