import type { HealthSignal } from '../types';

interface SignalsPanelProps {
  signal: HealthSignal | null;
}

const METRICS = [
  { key: 'sleep_hours', label: 'Sleep', unit: 'hours', icon: '🛌', max: 10 },
  { key: 'steps', label: 'Steps', unit: 'steps', icon: '🚶', max: 15000 },
  { key: 'stress_score', label: 'Stress', unit: 'score', icon: '😰', max: 100 },
  { key: 'heart_rate_rest', label: 'Heart Rate', unit: 'bpm', icon: '❤️', max: 120 },
] as const;

export function SignalsPanel({ signal }: SignalsPanelProps) {
  if (!signal) {
    return (
      <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-4">
        <h2 className="text-sm font-semibold text-slate-300 mb-3">Latest Signals</h2>
        <p className="text-sm text-slate-500">Waiting for data...</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-4">
      <h2 className="text-sm font-semibold text-slate-300 mb-3">Latest Signals</h2>
      <div className="space-y-3">
        {METRICS.map((m) => {
          const value = signal[m.key] as number;
          const pct = Math.min((value / m.max) * 100, 100);
          return (
            <div key={m.key}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs text-slate-400">
                  {m.icon} {m.label}
                </span>
                <span className="text-sm font-mono text-white">
                  {typeof value === 'number' ? value.toFixed(m.key === 'steps' ? 0 : 1) : value} {m.unit}
                </span>
              </div>
              <div className="w-full h-1.5 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full bg-cyan-400 transition-all duration-500"
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
