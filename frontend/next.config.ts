import type { NextConfig } from "next";

const imageServerPrefix =
  process.env.NEXT_PUBLIC_IMAGE_SERVER_PREFIX ?? "https://minio.localhost/public";

const imageServerUrl = (() => {
  try {
    return new URL(imageServerPrefix);
  } catch {
    return new URL("https://minio.localhost/public");
  }
})();

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: imageServerUrl.protocol.replace(":", ""),
        hostname: imageServerUrl.hostname,
        port: imageServerUrl.port || undefined,
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "cdn.example.com",
        pathname: "/**",
      },
    ],
  },
};

export default nextConfig;
