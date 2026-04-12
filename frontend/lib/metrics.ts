import { collectDefaultMetrics, Counter, Registry } from "prom-client";

type MetricsStore = {
  registry: Registry;
  httpRequestsTotal: Counter<"method" | "path" | "status">;
};

declare global {
  var __frontendMetricsStore: MetricsStore | undefined;
}

function createMetricsStore(): MetricsStore {
  const registry = new Registry();

  collectDefaultMetrics({ register: registry });

  const httpRequestsTotal = new Counter({
    name: "frontend_http_requests_total",
    help: "Total number of HTTP requests handled by the frontend.",
    labelNames: ["method", "path", "status"],
    registers: [registry],
  });

  return {
    registry,
    httpRequestsTotal,
  };
}

export function getMetricsStore(): MetricsStore {
  globalThis.__frontendMetricsStore ??= createMetricsStore();
  return globalThis.__frontendMetricsStore;
}
