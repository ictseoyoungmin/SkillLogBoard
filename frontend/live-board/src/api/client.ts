import type { CompareState, LiveConfig, LiveHealth, LiveState, LiveView } from "./types";

export class LiveApiError extends Error {
  status: number;
  body: string;
  path: string;

  constructor(message: string, status: number, body: string, path: string) {
    super(message);
    this.name = "LiveApiError";
    this.status = status;
    this.body = body;
    this.path = path;
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
    this.fetchImpl = options.fetchImpl ?? ((input, init) => fetch(input, init));
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
    let response: Response;
    try {
      response = await this.fetchImpl(`${this.baseUrl}${path}`, {
        headers: { Accept: "application/json" }
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : "network request failed";
      throw new LiveApiError(
        `Could not reach ${path}. Restart skilllog watch and refresh the browser. (${message})`,
        0,
        "",
        path
      );
    }
    if (!response.ok) {
      const body = await response.text();
      const detail = body.slice(0, 300).replace(/\s+/g, " ").trim();
      throw new LiveApiError(
        `Local API ${path} returned HTTP ${response.status}${detail ? `: ${detail}` : "."}`,
        response.status,
        body,
        path
      );
    }
    try {
      return (await response.json()) as T;
    } catch (err) {
      const message = err instanceof Error ? err.message : "invalid JSON";
      throw new LiveApiError(`Local API ${path} returned invalid JSON: ${message}`, response.status, "", path);
    }
  }
}

export const liveApi = new LiveApiClient();
