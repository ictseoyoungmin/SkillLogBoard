import React from "react";
import {
  LiveApiError,
  liveApi,
  type ArtifactRecord,
  type CompareSeries,
  type CompareState,
  type LiveConfig,
  type LiveState,
  type LiveView,
  type MetricCatalogItem,
  type MetricPoint,
  type RunSummary
} from "./api";

type ViewItem = {
  id: LiveView;
  label: string;
  group: "Project" | "Analysis" | "Evidence";
};

const VIEWS: ViewItem[] = [
  { id: "overview", label: "Overview", group: "Project" },
  { id: "runs", label: "Runs", group: "Project" },
  { id: "compare", label: "Compare", group: "Project" },
  { id: "lab", label: "Metric Lab", group: "Analysis" },
  { id: "artifacts", label: "Artifacts", group: "Analysis" },
  { id: "reports", label: "Reports", group: "Analysis" },
  { id: "agent", label: "Agent", group: "Evidence" },
  { id: "settings", label: "Settings", group: "Evidence" }
];

const GROUPS: ViewItem["group"][] = ["Project", "Analysis", "Evidence"];

function App() {
  const [config, setConfig] = React.useState<LiveConfig | null>(null);
  const [state, setState] = React.useState<LiveState | null>(null);
  const [compare, setCompare] = React.useState<CompareState | null>(null);
  const [activeView, setActiveView] = React.useState<LiveView>("overview");
  const [selectedMetric, setSelectedMetric] = React.useState<string>("");
  const [selectedRunIds, setSelectedRunIds] = React.useState<string[]>([]);
  const [query, setQuery] = React.useState("");
  const [error, setError] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [paletteOpen, setPaletteOpen] = React.useState(false);
  const [inspectorOpen, setInspectorOpen] = React.useState(false);

  const storageKey = React.useMemo(() => {
    const target = config?.target_dir ?? "pending";
    return `skilllogboard:v1.3:${config?.mode ?? "unknown"}:${target}`;
  }, [config]);

  React.useEffect(() => {
    let active = true;
    async function boot() {
      try {
        const nextConfig = await liveApi.config();
        if (!active) return;
        setConfig(nextConfig);
        setActiveView(nextConfig.default_view);
      } catch (err) {
        if (!active) return;
        setError(apiMessage(err));
        setLoading(false);
      }
    }
    void boot();
    return () => {
      active = false;
    };
  }, []);

  React.useEffect(() => {
    const saved = window.localStorage.getItem(storageKey);
    if (!saved) return;
    try {
      const parsed = JSON.parse(saved) as {
        activeView?: LiveView;
        selectedMetric?: string;
        selectedRunIds?: string[];
      };
      if (parsed.activeView && VIEWS.some((view) => view.id === parsed.activeView)) {
        setActiveView(parsed.activeView);
      }
      if (parsed.selectedMetric) setSelectedMetric(parsed.selectedMetric);
      if (Array.isArray(parsed.selectedRunIds)) setSelectedRunIds(parsed.selectedRunIds);
    } catch {
      window.localStorage.removeItem(storageKey);
    }
  }, [storageKey]);

  React.useEffect(() => {
    if (!config) return;
    window.localStorage.setItem(
      storageKey,
      JSON.stringify({ activeView, selectedMetric, selectedRunIds })
    );
  }, [activeView, config, selectedMetric, selectedRunIds, storageKey]);

  const refresh = React.useCallback(async () => {
    if (!config) return;
    setLoading(true);
    try {
      const nextState = await liveApi.state(activeView);
      setState(nextState);
      const metric =
        selectedMetric ||
        nextState.compare?.metric ||
        nextState.selected_metrics?.[0] ||
        nextState.metric_catalog?.[0]?.name ||
        "";
      if (!selectedMetric && metric) setSelectedMetric(metric);
      if (activeView === "compare" || activeView === "lab") {
        const nextCompare = await liveApi.compare({
          metric,
          runs: selectedRunIds,
          maxRuns: 6,
          maxPoints: 240,
          align: "step",
          normalize: false
        });
        setCompare(nextCompare);
        if (!selectedRunIds.length) setSelectedRunIds(nextCompare.selected_run_ids);
      } else {
        setCompare(nextState.compare ?? null);
      }
      setError(null);
    } catch (err) {
      setError(apiMessage(err));
    } finally {
      setLoading(false);
    }
  }, [activeView, config, selectedMetric, selectedRunIds]);

  React.useEffect(() => {
    void refresh();
  }, [refresh]);

  React.useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setPaletteOpen((value) => !value);
      }
      if (event.key === "Escape") {
        setPaletteOpen(false);
        setInspectorOpen(false);
      }
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  const runs = state?.runs ?? [];
  const metrics = state?.metric_catalog ?? [];
  const selectedRun = runs.find((run) => run.run_id === selectedRunIds[0]) ?? runs[0];

  return (
    <main className="app-shell" data-skilllogboard-ui="v1.3-react">
      <aside className="sidebar" aria-label="Live Board views">
        <Brand />
        {GROUPS.map((group) => (
          <nav className="nav-group" key={group} aria-label={group}>
            <div className="nav-label">{group}</div>
            {VIEWS.filter((view) => view.group === group).map((view) => (
              <button
                key={view.id}
                className="nav-item"
                data-active={activeView === view.id}
                type="button"
                onClick={() => setActiveView(view.id)}
              >
                {view.label}
              </button>
            ))}
          </nav>
        ))}
      </aside>
      <section className="workspace">
        <Topbar
          config={config}
          state={state}
          activeView={activeView}
          loading={loading}
          onRefresh={refresh}
          onPalette={() => setPaletteOpen(true)}
          onInspector={() => setInspectorOpen(true)}
        />
        {error ? <StateMessage tone="error" title="Local API unavailable" detail={error} /> : null}
        {loading && !state ? <StateMessage title="Loading local files" detail="Reading current state." /> : null}
        {state ? (
          <ViewRouter
            view={activeView}
            state={state}
            compare={compare}
            metricCatalog={metrics}
            selectedMetric={selectedMetric}
            selectedRunIds={selectedRunIds}
            query={query}
            onQuery={setQuery}
            onMetric={setSelectedMetric}
            onRunToggle={(runId) => setSelectedRunIds(toggle(selectedRunIds, runId, 6))}
            onView={setActiveView}
            onInspect={() => setInspectorOpen(true)}
          />
        ) : null}
      </section>
      <InspectorDrawer
        open={inspectorOpen}
        state={state}
        run={selectedRun}
        metric={metrics.find((item) => item.name === selectedMetric) ?? metrics[0]}
        onClose={() => setInspectorOpen(false)}
      />
      <CommandPalette
        open={paletteOpen}
        onClose={() => setPaletteOpen(false)}
        onView={(view) => {
          setActiveView(view);
          setPaletteOpen(false);
        }}
        onRefresh={() => {
          void refresh();
          setPaletteOpen(false);
        }}
      />
    </main>
  );
}

function Brand() {
  return (
    <div className="brand">
      <span className="brand-mark">S</span>
      <div>
        <strong>SkillLogBoard Live</strong>
        <span>Local evidence workspace</span>
      </div>
    </div>
  );
}

function Topbar(props: {
  config: LiveConfig | null;
  state: LiveState | null;
  activeView: LiveView;
  loading: boolean;
  onRefresh: () => void;
  onPalette: () => void;
  onInspector: () => void;
}) {
  const status = props.state?.status ?? props.state?.current_view ?? (props.loading ? "loading" : "ready");
  return (
    <header className="topbar">
      <div>
        <p className="eyebrow">{props.config?.mode ?? "local"} board</p>
        <h1>{labelForView(props.activeView)}</h1>
      </div>
      <div className="topbar-actions">
        <span className="status-pill">{status}</span>
        <button type="button" className="icon-button" onClick={props.onPalette} aria-label="Open command palette">
          K
        </button>
        <button type="button" className="icon-button" onClick={props.onInspector} aria-label="Open inspector">
          I
        </button>
        <button type="button" className="button" onClick={props.onRefresh}>
          Refresh
        </button>
      </div>
    </header>
  );
}

function ViewRouter(props: {
  view: LiveView;
  state: LiveState;
  compare: CompareState | null;
  metricCatalog: MetricCatalogItem[];
  selectedMetric: string;
  selectedRunIds: string[];
  query: string;
  onQuery: (value: string) => void;
  onMetric: (value: string) => void;
  onRunToggle: (runId: string) => void;
  onView: (view: LiveView) => void;
  onInspect: () => void;
}) {
  if (props.view === "runs") {
    return (
      <RunsView
        runs={props.state.runs ?? []}
        selectedRunIds={props.selectedRunIds}
        query={props.query}
        onQuery={props.onQuery}
        onRunToggle={props.onRunToggle}
        onInspect={props.onInspect}
      />
    );
  }
  if (props.view === "compare") {
    return (
      <CompareView
        compare={props.compare ?? props.state.compare ?? null}
        runs={props.state.runs ?? []}
        selectedRunIds={props.selectedRunIds}
        selectedMetric={props.selectedMetric}
        onRunToggle={props.onRunToggle}
        onMetric={props.onMetric}
      />
    );
  }
  if (props.view === "lab") {
    return (
      <MetricLabView
        metrics={props.metricCatalog}
        selectedMetric={props.selectedMetric}
        series={props.state.metric_series ?? []}
        compare={props.compare}
        onMetric={props.onMetric}
      />
    );
  }
  if (props.view === "artifacts") {
    return <ArtifactView title="Artifacts" artifacts={props.state.artifacts ?? []} />;
  }
  if (props.view === "reports") {
    return <ArtifactView title="Reports" artifacts={props.state.report_artifacts ?? []} />;
  }
  if (props.view === "agent") {
    return <AgentView state={props.state} />;
  }
  if (props.view === "settings") {
    return <SettingsView state={props.state} />;
  }
  return <OverviewView state={props.state} onView={props.onView} />;
}

function OverviewView({ state, onView }: { state: LiveState; onView: (view: LiveView) => void }) {
  const runs = state.runs ?? [];
  const capabilities = state.capabilities ?? {};
  const cards = [
    ["Runs", capabilities.run_count ?? runs.length ?? (state.mode === "run" ? 1 : 0)],
    ["Metrics", capabilities.metric_count ?? state.metric_catalog?.length ?? 0],
    ["Artifacts", capabilities.artifact_count ?? state.artifacts?.length ?? 0],
    ["Warnings", capabilities.warning_count ?? state.warnings?.length ?? state.alerts?.length ?? 0]
  ];
  return (
    <div className="view-stack">
      <section className="summary-grid" aria-label="Local project summary">
        {cards.map(([label, value]) => (
          <article key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </article>
        ))}
      </section>
      <section className="split-grid">
        <div className="panel">
          <PanelHead title="Leaderboard" action="Open compare" onAction={() => onView("compare")} />
          <DataTable
            columns={["run_id", "metric", "value", "status"]}
            rows={(state.leaderboard ?? []).slice(0, 8).map((row) => ({
              run_id: String(row.run_id ?? ""),
              metric: String(row.metric ?? ""),
              value: String(row.value ?? ""),
              status: String(row.status ?? "")
            }))}
            empty="No leaderboard rows"
          />
        </div>
        <div className="panel">
          <PanelHead title="Recent Runs" action="Open runs" onAction={() => onView("runs")} />
          <RunList runs={runs.slice(0, 5)} />
        </div>
      </section>
    </div>
  );
}

function RunsView(props: {
  runs: RunSummary[];
  selectedRunIds: string[];
  query: string;
  onQuery: (value: string) => void;
  onRunToggle: (runId: string) => void;
  onInspect: () => void;
}) {
  const rows = props.runs.filter((run) =>
    [run.run_id, run.run_name, run.status, run.group].join(" ").toLowerCase().includes(props.query.toLowerCase())
  );
  return (
    <section className="panel">
      <PanelHead title="Runs" action="Inspect" onAction={props.onInspect} />
      <div className="toolbar">
        <input
          type="search"
          value={props.query}
          onChange={(event) => props.onQuery(event.currentTarget.value)}
          placeholder="Filter runs"
          aria-label="Filter runs"
        />
        <span className="meta">{props.selectedRunIds.length} selected</span>
      </div>
      <DataTable
        columns={["selected", "run_id", "run_name", "status", "artifact_count", "warning_count"]}
        rows={rows.map((run) => ({
          selected: (
            <input
              type="checkbox"
              checked={props.selectedRunIds.includes(run.run_id)}
              onChange={() => props.onRunToggle(run.run_id)}
              aria-label={`Select ${run.run_id}`}
            />
          ),
          run_id: run.run_id,
          run_name: run.run_name ?? "",
          status: run.status ?? "",
          artifact_count: run.artifact_count ?? 0,
          warning_count: run.warning_count ?? 0
        }))}
        empty="No runs indexed"
      />
    </section>
  );
}

function CompareView(props: {
  compare: CompareState | null;
  runs: RunSummary[];
  selectedRunIds: string[];
  selectedMetric: string;
  onRunToggle: (runId: string) => void;
  onMetric: (value: string) => void;
}) {
  const compare = props.compare;
  const metrics = compare?.shared_metrics ?? [];
  return (
    <div className="view-stack">
      <section className="panel">
        <PanelHead title="Compare" />
        <div className="toolbar">
          <select
            value={props.selectedMetric || compare?.metric || ""}
            onChange={(event) => props.onMetric(event.currentTarget.value)}
            aria-label="Compare metric"
          >
            {(metrics.length ? metrics : [props.selectedMetric || compare?.metric || ""]).map((metric) => (
              <option key={metric} value={metric}>
                {metric}
              </option>
            ))}
          </select>
          <span className="meta">{compare?.selected_run_ids.length ?? 0} runs</span>
          <span className="meta">{compare?.bounds.max_points ?? 0} max points</span>
        </div>
        <SeriesChart series={compare?.series ?? []} />
      </section>
      <section className="panel">
        <PanelHead title="Run Selection" />
        <div className="run-picker-grid">
          {props.runs.slice(0, 12).map((run) => (
            <label className="check-row" key={run.run_id}>
              <input
                type="checkbox"
                checked={props.selectedRunIds.includes(run.run_id)}
                onChange={() => props.onRunToggle(run.run_id)}
              />
              <span>{run.run_name || run.run_id}</span>
              <em>{run.status}</em>
            </label>
          ))}
        </div>
      </section>
    </div>
  );
}

function MetricLabView(props: {
  metrics: MetricCatalogItem[];
  selectedMetric: string;
  series: MetricPoint[];
  compare: CompareState | null;
  onMetric: (value: string) => void;
}) {
  const selected = props.selectedMetric || props.metrics[0]?.name || "";
  const localSeries = selected
    ? [
        {
          run_id: "current",
          metric: selected,
          points: props.series
            .filter((point) => "name" in point ? String((point as { name?: unknown }).name) === selected : true)
            .map((point, index) => ({
              x: typeof point.step === "number" ? point.step : index,
              y: typeof point.value === "number" ? point.value : typeof point.y === "number" ? point.y : null
            }))
        }
      ]
    : [];
  return (
    <div className="metric-layout">
      <section className="panel metric-catalog">
        <PanelHead title="Metric Catalog" />
        {props.metrics.map((metric) => (
          <button
            className="metric-row"
            data-active={metric.name === selected}
            key={metric.name}
            type="button"
            onClick={() => props.onMetric(metric.name)}
          >
            <span>{metric.name}</span>
            <em>{formatNumber(metric.latest)}</em>
          </button>
        ))}
      </section>
      <section className="panel">
        <PanelHead title={selected || "Metric"} />
        <SeriesChart series={props.compare?.series?.length ? props.compare.series : localSeries} />
      </section>
    </div>
  );
}

function ArtifactView({ title, artifacts }: { title: string; artifacts: ArtifactRecord[] }) {
  return (
    <section className="panel">
      <PanelHead title={title} />
      <div className="artifact-grid">
        {artifacts.length ? (
          artifacts.map((artifact, index) => (
            <article className="artifact-card" key={`${artifact.path ?? artifact.name ?? index}`}>
              <strong>{artifact.name ?? artifact.path ?? "artifact"}</strong>
              <span>{artifact.type ?? "file"}</span>
              <code>{artifact.path ?? ""}</code>
            </article>
          ))
        ) : (
          <EmptyState title={`No ${title.toLowerCase()}`} />
        )}
      </div>
    </section>
  );
}

function AgentView({ state }: { state: LiveState }) {
  const agent = state.agent_workspace ?? {};
  return (
    <section className="panel">
      <PanelHead title="Agent Evidence" />
      <section className="summary-grid compact">
        <article>
          <span>Actions</span>
          <strong>{agent.actions_count ?? 0}</strong>
        </article>
        <article>
          <span>Status</span>
          <strong>{agent.latest_status || "none"}</strong>
        </article>
        <article>
          <span>Handoff</span>
          <strong>{agent.handoff ? "yes" : "no"}</strong>
        </article>
        <article>
          <span>Decisions</span>
          <strong>{agent.decisions ? "yes" : "no"}</strong>
        </article>
      </section>
      <DataTable
        columns={["file"]}
        rows={(agent.files_changed ?? []).map((file) => ({ file }))}
        empty="No changed files logged"
      />
    </section>
  );
}

function SettingsView({ state }: { state: LiveState }) {
  const rows = [
    { key: "mode", value: state.mode },
    { key: "current_view", value: state.current_view ?? "" },
    { key: "payload_scope", value: state.payload_scope ?? "" },
    { key: "root_dir", value: state.root_dir ?? state.run_dir ?? "" }
  ];
  return (
    <section className="panel">
      <PanelHead title="Local Settings" />
      <DataTable columns={["key", "value"]} rows={rows} empty="No settings" />
    </section>
  );
}

function InspectorDrawer(props: {
  open: boolean;
  state: LiveState | null;
  run?: RunSummary;
  metric?: MetricCatalogItem;
  onClose: () => void;
}) {
  return (
    <aside className="drawer" data-open={props.open} aria-hidden={!props.open} aria-label="Inspector drawer">
      <div className="drawer-head">
        <strong>Inspector</strong>
        <button type="button" className="icon-button" onClick={props.onClose} aria-label="Close inspector">
          X
        </button>
      </div>
      <div className="drawer-body">
        <KeyValue title="Run" values={props.run ?? { run_id: "none" }} />
        <KeyValue title="Metric" values={props.metric ?? { name: "none" }} />
        <KeyValue title="State" values={{ mode: props.state?.mode ?? "", scope: props.state?.payload_scope ?? "" }} />
      </div>
    </aside>
  );
}

function CommandPalette(props: {
  open: boolean;
  onClose: () => void;
  onView: (view: LiveView) => void;
  onRefresh: () => void;
}) {
  if (!props.open) return null;
  return (
    <div className="palette-backdrop" role="presentation" onMouseDown={props.onClose}>
      <section className="palette" role="dialog" aria-modal="true" aria-label="Command palette" onMouseDown={(event) => event.stopPropagation()}>
        <div className="palette-head">Command Palette</div>
        <button type="button" onClick={props.onRefresh}>Refresh local state</button>
        {VIEWS.map((view) => (
          <button type="button" key={view.id} onClick={() => props.onView(view.id)}>
            Open {view.label}
          </button>
        ))}
      </section>
    </div>
  );
}

function SeriesChart({ series }: { series: Array<Pick<CompareSeries, "run_id" | "points">> }) {
  const width = 900;
  const height = 320;
  const values = series.flatMap((item) => item.points.map(pointValue).filter(isNumber));
  const xs = series.flatMap((item) => item.points.map(pointX).filter(isNumber));
  if (!series.length || !values.length || !xs.length) return <EmptyState title="No chart data" />;
  const minY = Math.min(...values);
  const maxY = Math.max(...values);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const colors = ["#0b7285", "#2563eb", "#7c3aed", "#c2410c", "#15803d", "#be123c"];
  return (
    <svg className="chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Metric chart">
      <line x1="42" y1="286" x2="870" y2="286" />
      <line x1="42" y1="28" x2="42" y2="286" />
      {series.map((item, index) => {
        const points = item.points
          .map((point, pointIndex) => {
            const x = pointX(point) ?? pointIndex;
            const y = pointValue(point);
            if (y === null) return "";
            return `${scale(x, minX, maxX, 52, 860)},${scale(y, minY, maxY, 276, 38)}`;
          })
          .filter(Boolean)
          .join(" ");
        return <polyline key={item.run_id} points={points} stroke={colors[index % colors.length]} />;
      })}
    </svg>
  );
}

function DataTable({
  columns,
  rows,
  empty
}: {
  columns: string[];
  rows: Array<Record<string, React.ReactNode>>;
  empty: string;
}) {
  if (!rows.length) return <EmptyState title={empty} />;
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>{columns.map((column) => <th key={column}>{column.replaceAll("_", " ")}</th>)}</tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={index}>
              {columns.map((column) => <td key={column}>{row[column] ?? ""}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function RunList({ runs }: { runs: RunSummary[] }) {
  if (!runs.length) return <EmptyState title="No runs indexed" />;
  return (
    <div className="run-list">
      {runs.map((run) => (
        <article key={run.run_id}>
          <strong>{run.run_name || run.run_id}</strong>
          <span>{run.status}</span>
        </article>
      ))}
    </div>
  );
}

function PanelHead({ title, action, onAction }: { title: string; action?: string; onAction?: () => void }) {
  return (
    <div className="panel-head">
      <h2>{title}</h2>
      {action && onAction ? <button type="button" className="button subtle" onClick={onAction}>{action}</button> : null}
    </div>
  );
}

function EmptyState({ title }: { title: string }) {
  return <div className="empty-state">{title}</div>;
}

function StateMessage({ title, detail, tone }: { title: string; detail: string; tone?: "error" }) {
  return (
    <div className={tone === "error" ? "error-state" : "empty-state"} role={tone === "error" ? "alert" : "status"}>
      <strong>{title}</strong>
      <span>{detail}</span>
    </div>
  );
}

function KeyValue({ title, values }: { title: string; values: object }) {
  return (
    <section className="kv">
      <h3>{title}</h3>
      {Object.entries(values as Record<string, unknown>).slice(0, 8).map(([key, value]) => (
        <div key={key}>
          <span>{key}</span>
          <code>{String(value ?? "")}</code>
        </div>
      ))}
    </section>
  );
}

function apiMessage(err: unknown) {
  return err instanceof LiveApiError ? err.message : "Could not read local Live Board files.";
}

function labelForView(view: LiveView) {
  return VIEWS.find((item) => item.id === view)?.label ?? "Live Board";
}

function toggle(values: string[], value: string, limit: number) {
  if (values.includes(value)) return values.filter((item) => item !== value);
  return [...values, value].slice(-limit);
}

function pointValue(point: MetricPoint): number | null {
  if (typeof point.y === "number") return point.y;
  if (typeof point.value === "number") return point.value;
  return null;
}

function pointX(point: MetricPoint): number | null {
  if (typeof point.x === "number") return point.x;
  if (typeof point.step === "number") return point.step;
  return null;
}

function isNumber(value: number | null): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

function scale(value: number, min: number, max: number, outMin: number, outMax: number) {
  if (max === min) return (outMin + outMax) / 2;
  const ratio = (value - min) / (max - min);
  return outMin + ratio * (outMax - outMin);
}

function formatNumber(value: unknown) {
  return typeof value === "number" ? value.toFixed(Math.abs(value) >= 10 ? 1 : 4) : "";
}

export default App;
