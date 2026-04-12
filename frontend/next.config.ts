import type { NextConfig } from "next";
import type { RemotePattern } from "next/dist/shared/lib/image-config";

const imageServerPrefix =
  process.env.NEXT_PUBLIC_IMAGE_SERVER_PREFIX ?? "https://minio.localhost/public";

const imageServerUrl = (() => {
  try {
    return new URL(imageServerPrefix);
  } catch {
    return new URL("https://minio.localhost/public");
  }
})();

const imageServerPattern: RemotePattern = {
  protocol: imageServerUrl.protocol === "http:" ? "http" : "https",
  hostname: imageServerUrl.hostname,
  pathname: "/**",
  ...(imageServerUrl.port ? { port: imageServerUrl.port } : {}),
};

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      imageServerPattern,
      {
        protocol: "https",
        hostname: "cdn.example.com",
        pathname: "/**",
      },
    ],
  },
};

export default nextConfig;
