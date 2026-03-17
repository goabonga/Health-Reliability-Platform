import type { Action } from '../types';

interface ActionsPanelProps {
  actions: Action[];
}

export function ActionsPanel({ actions }: ActionsPanelProps) {
  const recent = actions.slice(-10).reverse();

  return (
    <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-4">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold text-slate-300">Remediation Actions</h2>
        <span className="text-xs text-slate-500">{actions.length} total</span>
      </div>
      {recent.length === 0 ? (
        <p className="text-sm text-slate-500">No actions yet</p>
      ) : (
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {recent.map((action) => (
            <div
              key={action.id}
              className="flex items-start gap-3 bg-slate-900/50 rounded-md border border-slate-700 p-3"
            >
              <div className="w-6 h-6 rounded-full bg-purple-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                <span className="text-[10px] text-purple-400">AI</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-white">{action.description}</p>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-[10px] text-purple-400">{action.agent}</span>
                  <span className="text-[10px] text-slate-600">
                    {new Date(action.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
