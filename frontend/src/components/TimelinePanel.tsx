import type { TimelineEvent } from '../types';

interface TimelinePanelProps {
  events: TimelineEvent[];
}

const TYPE_COLORS: Record<string, string> = {
  signal: 'bg-cyan-500',
  slo: 'bg-yellow-500',
  incident: 'bg-red-500',
  agent: 'bg-purple-500',
  action: 'bg-emerald-500',
  system: 'bg-slate-500',
};

const TYPE_LABELS: Record<string, string> = {
  signal: 'SIG',
  slo: 'SLO',
  incident: 'INC',
  agent: 'AGT',
  action: 'ACT',
  system: 'SYS',
};

export function TimelinePanel({ events }: TimelinePanelProps) {
  const recent = events.slice(0, 30);

  return (
    <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-4">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold text-slate-300">Timeline</h2>
        <span className="text-xs text-slate-500">{events.length} events</span>
      </div>
      {recent.length === 0 ? (
        <p className="text-sm text-slate-500">No events yet</p>
      ) : (
        <div className="space-y-1.5 max-h-96 overflow-y-auto">
          {recent.map((event, i) => (
            <div key={i} className="flex items-start gap-2 py-1">
              <span
                className={`text-[9px] px-1.5 py-0.5 rounded font-mono font-bold text-white flex-shrink-0 ${TYPE_COLORS[event.event_type]}`}
              >
                {TYPE_LABELS[event.event_type]}
              </span>
              <p className="text-xs text-slate-300 flex-1 leading-relaxed">
                {event.message}
              </p>
              <span className="text-[10px] text-slate-600 flex-shrink-0">
                {new Date(event.timestamp).toLocaleTimeString()}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
