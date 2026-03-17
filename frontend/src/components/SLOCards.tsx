import type { SLOResult } from '../types';

interface SLOCardsProps {
  slos: SLOResult[];
}

export function SLOCards({ slos }: SLOCardsProps) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
      {slos.map((slo) => (
        <div
          key={slo.slo_name}
          className={`rounded-lg border p-4 ${
            slo.passed
              ? 'bg-emerald-500/10 border-emerald-500/30'
              : 'bg-red-500/10 border-red-500/30'
          }`}
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
              {slo.metric.replace('_', ' ')}
            </span>
            <span
              className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                slo.passed
                  ? 'bg-emerald-500/20 text-emerald-400'
                  : 'bg-red-500/20 text-red-400'
              }`}
            >
              {slo.passed ? 'PASS' : 'FAIL'}
            </span>
          </div>
          <div className="text-2xl font-bold text-white">
            {slo.current_value.toFixed(1)}
          </div>
          <div className="text-xs text-slate-500 mt-1">
            threshold: {slo.operator} {slo.threshold}
          </div>
        </div>
      ))}
    </div>
  );
}
