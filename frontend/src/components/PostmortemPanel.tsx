interface Postmortem {
  incident_id: string;
  title: string;
  summary: string;
  root_cause: string;
  impact: string;
  lessons_learned: string[];
  action_items: string[];
  timestamp: string;
}

interface PostmortemPanelProps {
  postmortems: Postmortem[];
}

export function PostmortemPanel({ postmortems }: PostmortemPanelProps) {
  const recent = postmortems.slice(-5).reverse();

  return (
    <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-4">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold text-slate-300">Postmortems</h2>
        <span className="text-xs text-slate-500">{postmortems.length} total</span>
      </div>
      {recent.length === 0 ? (
        <p className="text-sm text-slate-500">No postmortems yet. They are generated when incidents are resolved.</p>
      ) : (
        <div className="space-y-3 max-h-80 overflow-y-auto">
          {recent.map((pm, i) => (
            <div key={i} className="bg-slate-900/50 rounded-md border border-slate-700 p-3">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-medium">
                  RESOLVED
                </span>
                <span className="text-[10px] text-slate-600">
                  {new Date(pm.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <p className="text-sm font-medium text-white mb-1">{pm.title}</p>
              <p className="text-xs text-slate-400 mb-2">{pm.summary}</p>
              <div className="space-y-1.5">
                <div>
                  <span className="text-[10px] text-slate-500 uppercase tracking-wider">Root Cause</span>
                  <p className="text-xs text-slate-300">{pm.root_cause}</p>
                </div>
                <div>
                  <span className="text-[10px] text-slate-500 uppercase tracking-wider">Lessons Learned</span>
                  <ul className="text-xs text-slate-300 list-disc list-inside">
                    {pm.lessons_learned.map((l, j) => (
                      <li key={j}>{l}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
