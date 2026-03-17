import { usePolling } from '../hooks/useApi';

interface ScenarioStatus {
  active_scenario: string | null;
  step: number;
  total_steps: number;
  available: string[];
}

const SCENARIO_LABELS: Record<string, string> = {
  sleep_degradation: 'Sleep Degradation',
  recovery: 'Recovery Path',
  low_activity: 'Low Activity',
};

export function ScenarioSelector() {
  const { data: status, refetch } = usePolling<ScenarioStatus>('/scenarios', 5000);

  const activate = async (name: string) => {
    await fetch(`/api/scenarios/${name}`, { method: 'POST' });
    refetch();
  };

  const stop = async () => {
    await fetch('/api/scenarios/stop', { method: 'POST' });
    refetch();
  };

  return (
    <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-4">
      <h2 className="text-sm font-semibold text-slate-300 mb-3">Demo Scenarios</h2>
      <div className="flex flex-wrap gap-2">
        {status?.available.map((name) => (
          <button
            key={name}
            onClick={() => activate(name)}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
              status?.active_scenario === name
                ? 'bg-cyan-500 text-white'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            {SCENARIO_LABELS[name] ?? name}
          </button>
        ))}
        {status?.active_scenario && (
          <button
            onClick={stop}
            className="px-3 py-1.5 rounded-md text-xs font-medium bg-red-500/20 text-red-400 hover:bg-red-500/30 transition-colors"
          >
            Stop
          </button>
        )}
      </div>
      {status?.active_scenario && (
        <div className="mt-2 text-xs text-slate-500">
          Step {status.step}/{status.total_steps} — {SCENARIO_LABELS[status.active_scenario]}
        </div>
      )}
    </div>
  );
}
