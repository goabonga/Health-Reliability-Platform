import type { Incident } from '../types';

interface IncidentsPanelProps {
  incidents: Incident[];
}

const SEVERITY_COLORS: Record<string, string> = {
  critical: 'bg-red-500/20 text-red-400 border-red-500/30',
  high: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  low: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
};

const STATUS_COLORS: Record<string, string> = {
  open: 'text-red-400',
  mitigated: 'text-yellow-400',
  resolved: 'text-emerald-400',
};

export function IncidentsPanel({ incidents }: IncidentsPanelProps) {
  const recent = incidents.slice(-10).reverse();

  return (
    <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-4">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold text-slate-300">Incidents</h2>
        <span className="text-xs text-slate-500">{incidents.length} total</span>
      </div>
      {recent.length === 0 ? (
        <p className="text-sm text-slate-500">No incidents</p>
      ) : (
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {recent.map((inc) => (
            <div
              key={inc.id}
              className="bg-slate-900/50 rounded-md border border-slate-700 p-3"
            >
              <div className="flex items-center gap-2 mb-1">
                <span
                  className={`text-[10px] px-1.5 py-0.5 rounded font-medium border ${SEVERITY_COLORS[inc.severity]}`}
                >
                  {inc.severity.toUpperCase()}
                </span>
                <span className={`text-[10px] font-medium ${STATUS_COLORS[inc.status]}`}>
                  {inc.status.toUpperCase()}
                </span>
              </div>
              <p className="text-sm text-white font-medium">{inc.title}</p>
              <p className="text-xs text-slate-400 mt-1">{inc.description}</p>
              <p className="text-[10px] text-slate-600 mt-1">
                {new Date(inc.timestamp).toLocaleTimeString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
