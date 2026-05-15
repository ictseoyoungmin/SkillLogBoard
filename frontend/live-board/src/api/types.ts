export type LiveMode = "run" | "project";
export type LiveView =
  | "overview"
  | "runs"
  | "compare"
  | "lab"
  | "artifacts"
  | "reports"
  | "agent"
  | "settings";

export type StatusCounts = Record<string, number>;

export interface LiveHealth {
  ok: boolean;
  mode: LiveMode;
  default_view: LiveView;
  views: LiveView[];
  target_dir: string;
  poll_interval: number;
  latest: boolean;
  monitor_system: boolean;
  monitor_gpu: boolean;
}

export type LiveConfig = Omit<LiveHealth, "ok">;

export interface MetricCatalogItem {
  name: string;
  group?: string;
  count?: number;
  latest?: number | null;
  min?: number | null;
  max?: number | null;
  first_step?: number | null;
  last_step?: number | null;
  pinned?: boolean;
}

export interface MetricPoint {
  step?: number | null;
  x?: number | null;
  value?: number | null;
  y?: number | null;
  timestamp?: string | null;
}

export interface RunSummary {
  run_id: string;
  run_name?: string;
  run_dir?: string;
  project?: string;
  status?: string;
  metrics?: Record<string, number | string | null>;
  metric_catalog?: MetricCatalogItem[];
  best_metric?: Record<string, unknown> | null;
  main_metric?: Record<string, unknown> | null;
  tags?: string[];
  group?: string;
  baseline?: boolean;
  branch?: string;
  updated?: number;
  artifact_count?: number;
  report_artifact_count?: number;
  agent_evidence?: boolean;
  warning_count?: number;
  warnings?: string[];
}

export interface CompareRun {
  run_id: string;
  run_name?: string;
  status?: string;
  role?: string;
  roles?: string[];
  metric?: string | null;
}

export interface CompareSeries {
  run_id: string;
  run_name?: string;
  status?: string;
  role?: string;
  roles?: string[];
  metric?: string | null;
  visible?: boolean;
  points: MetricPoint[];
  point_count?: number;
}

export interface CompareState {
  metric: string | null;
  align: "step" | "relative";
  normalize: boolean;
  bounds: {
    max_runs: number;
    max_points: number;
  };
  runs: CompareRun[];
  selected_run_ids: string[];
  shared_metrics: string[];
  series: CompareSeries[];
  warnings: string[];
}

export interface ArtifactRecord {
  type?: string;
  name?: string;
  path?: string;
  size?: number;
  modified?: number;
  preview?: string;
  [key: string]: unknown;
}

export interface AgentWorkspace {
  actions_count?: number;
  latest_action?: Record<string, unknown>;
  latest_status?: string;
  latest_target?: string;
  files_changed?: string[];
  handoff?: boolean;
  decisions?: boolean;
}

export interface Capabilities {
  mode?: LiveMode;
  run_count?: number;
  metric_count?: number;
  shared_metric_count?: number;
  event_count?: number;
  rule_count?: number;
  artifact_count?: number;
  report_artifact_count?: number;
  warning_count?: number;
  agent_evidence?: boolean;
  compare_ready?: boolean;
}

export interface LiveState {
  mode: LiveMode;
  current_view?: LiveView;
  payload_scope?: "summary" | "series";
  run_dir?: string;
  root_dir?: string;
  status?: string;
  manifest?: Record<string, unknown>;
  metrics?: Record<string, unknown>;
  metric_series?: MetricPoint[];
  metric_catalog?: MetricCatalogItem[];
  selected_metrics?: string[];
  pinned_metrics?: string[];
  context_markers?: Record<string, unknown>[];
  report_artifacts?: ArtifactRecord[];
  artifact_groups?: Record<string, ArtifactRecord[]>;
  agent_workspace?: AgentWorkspace;
  capabilities?: Capabilities;
  runs?: RunSummary[];
  status_counts?: StatusCounts;
  alerts?: string[];
  leaderboard?: Record<string, unknown>[];
  compare?: CompareState;
  compare_candidates?: CompareRun[];
  shared_metrics?: string[];
  warnings?: string[];
  logs?: string[];
  events?: Record<string, unknown>[];
  rules?: Record<string, unknown>[];
  artifacts?: ArtifactRecord[];
  monitoring?: Record<string, unknown>[];
}
