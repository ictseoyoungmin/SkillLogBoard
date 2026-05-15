import type { CompareState, LiveConfig, LiveHealth, LiveState, LiveView } from "./types";

export class LiveApiError extends Error {
  status: number;
  body: string;

  constructor(message: string, status: number, body: string) {
    super(message);
    this.name = "LiveApiError";
    this.status = status;
    this.body = body;
  }
}

export interface LiveApiClientOptions {
  baseUrl?: string;
  fetchImpl?: typeof fetch;
}

export interface CompareQuery {
  metric?: string | null;
  runs?: string[];
  maxRuns?: number;
  maxPoints?: number;
  normalize?: boolean;
  align?: "step" | "relative";
}

export class LiveApiClient {
  private readonly baseUrl: string;
  private readonly fetchImpl: typeof fetch;

  constructor(options: LiveApiClientOptions = {}) {
    this.baseUrl = options.baseUrl ?? "";
    this.fetchImpl = options.fetchImpl ?? fetch;
  }

  health(): Promise<LiveHealth> {
    return this.fetchJson<LiveHealth>("/api/health");
  }

  config(): Promise<LiveConfig> {
    return this.fetchJson<LiveConfig>("/api/config");
  }

  state(view?: LiveView): Promise<LiveState> {
    const query = view ? `?view=${encodeURIComponent(view)}` : "";
    return this.fetchJson<LiveState>(`/api/state${query}`);
  }

  compare(query: CompareQuery = {}): Promise<CompareState> {
    const params = new URLSearchParams();
    if (query.metric) params.set("metric", query.metric);
    if (query.runs?.length) params.set("runs", query.runs.join(","));
    if (query.maxRuns) params.set("max_runs", String(query.maxRuns));
    if (query.maxPoints) params.set("max_points", String(query.maxPoints));
    if (typeof query.normalize === "boolean") params.set("normalize", String(query.normalize));
    if (query.align) params.set("align", query.align);
    const suffix = params.toString() ? `?${params.toString()}` : "";
    return this.fetchJson<CompareState>(`/api/compare${suffix}`);
  }

  private async fetchJson<T>(path: string): Promise<T> {
    const response = await this.fetchImpl(`${this.baseUrl}${path}`, {
      headers: { Accept: "application/json" }
    });
    if (!response.ok) {
      const body = await response.text();
      throw new LiveApiError(
        `Could not read local SkillLogBoard API ${path}. Check that skilllog watch is still running.`,
        response.status,
        body
      );
    }
    return (await response.json()) as T;
  }
}

export const liveApi = new LiveApiClient();
