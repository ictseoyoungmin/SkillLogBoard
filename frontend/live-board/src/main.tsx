import React from "react";
import { createRoot } from "react-dom/client";
import { LiveApiError, liveApi, type LiveConfig, type LiveState } from "./api";
import "./styles.css";

function App() {
  const [config, setConfig] = React.useState<LiveConfig | null>(null);
  const [state, setState] = React.useState<LiveState | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    let active = true;
    async function load() {
      try {
        const nextConfig = await liveApi.config();
        const nextState = await liveApi.state(nextConfig.default_view);
        if (!active) return;
        setConfig(nextConfig);
        setState(nextState);
        setError(null);
      } catch (err) {
        if (!active) return;
        setError(err instanceof LiveApiError ? err.message : "Could not read local Live Board files.");
      }
    }
    void load();
    return () => {
      active = false;
    };
  }, []);

  const runCount = state?.runs?.length ?? (state?.mode === "run" ? 1 : 0);
  const metricCount = state?.metric_catalog?.length ?? state?.capabilities?.metric_count ?? 0;
  const target = config?.target_dir ?? state?.root_dir ?? state?.run_dir ?? "Local workspace";

  return (
    <main className="app-shell" data-skilllogboard-ui="v1.3-react">
      <aside className="sidebar" aria-label="Live Board views">
        <div className="brand">
          <span className="brand-mark">S</span>
          <div>
            <strong>SkillLogBoard Live</strong>
            <span>Local evidence workspace</span>
          </div>
        </div>
        {["Overview", "Runs", "Compare", "Metric Lab", "Artifacts", "Reports", "Agent", "Settings"].map(
          (item) => (
            <button key={item} className="nav-item" type="button">
              {item}
            </button>
          )
        )}
      </aside>
      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">{config?.mode ?? "loading"} board</p>
            <h1>Commercial Live UI</h1>
          </div>
          <span className="status-pill">{state?.status ?? state?.current_view ?? "loading"}</span>
        </header>
        {error ? <div className="error-state" role="alert">{error}</div> : null}
        <section className="summary-grid" aria-label="Local project summary">
          <article>
            <span>Target</span>
            <strong>{target}</strong>
          </article>
          <article>
            <span>Runs</span>
            <strong>{runCount}</strong>
          </article>
          <article>
            <span>Metrics</span>
            <strong>{metricCount}</strong>
          </article>
          <article>
            <span>Warnings</span>
            <strong>{state?.warnings?.length ?? state?.alerts?.length ?? 0}</strong>
          </article>
        </section>
        <section className="panel" aria-label="Frontend readiness">
          <h2>React shell connected</h2>
          <p>
            This v1.3 frontend source reads the local REST API and builds into the Python package.
            Detailed commercial views are layered on this shell in the next slices.
          </p>
        </section>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
