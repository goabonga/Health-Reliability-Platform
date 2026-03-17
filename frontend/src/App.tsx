import { Header } from './components/Header';
import { SLOCards } from './components/SLOCards';
import { SignalsPanel } from './components/SignalsPanel';
import { IncidentsPanel } from './components/IncidentsPanel';
import { ActionsPanel } from './components/ActionsPanel';
import { TimelinePanel } from './components/TimelinePanel';
import { usePolling } from './hooks/useApi';
import type { SystemState, SLOResult, TimelineEvent } from './types';

function App() {
  const { data: state } = usePolling<SystemState>('/state', 5000);
  const { data: slos } = usePolling<SLOResult[]>('/slo/evaluate', 5000);
  const { data: timeline } = usePolling<TimelineEvent[]>('/timeline', 5000);
  const { data: orchestratorStatus } = usePolling<{ running: boolean }>('/orchestrator/status', 5000);

  return (
    <div className="min-h-screen bg-slate-900">
      <Header
        orchestratorRunning={orchestratorStatus?.running ?? false}
        incidentCount={state?.open_incidents?.length ?? 0}
        agentCount={5}
      />

      <main className="p-6 space-y-6 max-w-7xl mx-auto">
        {/* SLO Overview */}
        <section>
          <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">
            SLO Status
          </h2>
          <SLOCards slos={slos ?? []} />
        </section>

        {/* Grid layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left column */}
          <div className="space-y-6">
            <SignalsPanel signal={state?.latest_signal ?? null} />
            <ActionsPanel actions={state?.recent_actions ?? []} />
          </div>

          {/* Center column */}
          <div>
            <IncidentsPanel incidents={state?.open_incidents ?? []} />
          </div>

          {/* Right column */}
          <div>
            <TimelinePanel events={timeline ?? []} />
          </div>
        </div>

        {/* Stats bar */}
        <div className="grid grid-cols-3 gap-3">
          <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-3 text-center">
            <div className="text-2xl font-bold text-cyan-400">{state?.total_signals ?? 0}</div>
            <div className="text-xs text-slate-500">Signals Processed</div>
          </div>
          <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-3 text-center">
            <div className="text-2xl font-bold text-red-400">{state?.total_incidents ?? 0}</div>
            <div className="text-xs text-slate-500">Total Incidents</div>
          </div>
          <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-3 text-center">
            <div className="text-2xl font-bold text-purple-400">{state?.total_actions ?? 0}</div>
            <div className="text-xs text-slate-500">Actions Taken</div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
