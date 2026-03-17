interface HeaderProps {
  orchestratorRunning: boolean;
  incidentCount: number;
  agentCount: number;
}

export function Header({ orchestratorRunning, incidentCount, agentCount }: HeaderProps) {
  const systemHealth = incidentCount === 0 ? 'healthy' : incidentCount <= 2 ? 'degraded' : 'critical';
  const healthColors = {
    healthy: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
    degraded: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    critical: 'bg-red-500/20 text-red-400 border-red-500/30',
  };
  const healthLabels = {
    healthy: 'All Systems Healthy',
    degraded: 'Degraded',
    critical: 'Critical',
  };

  return (
    <header className="bg-slate-800/50 border-b border-slate-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center text-white font-bold text-sm">
            HR
          </div>
          <div>
            <h1 className="text-lg font-semibold text-white">Health Reliability Platform</h1>
            <p className="text-xs text-slate-400">SRE-style health observability</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          {/* System Health */}
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full border ${healthColors[systemHealth]}`}>
            <div className={`w-2 h-2 rounded-full ${systemHealth === 'healthy' ? 'bg-emerald-400' : systemHealth === 'degraded' ? 'bg-yellow-400' : 'bg-red-400 animate-pulse'}`} />
            <span className="text-xs font-medium">{healthLabels[systemHealth]}</span>
          </div>

          {/* AI Operators */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-purple-500/30 bg-purple-500/10">
            <span className="text-xs text-purple-400 font-medium">{agentCount} AI Operators Active</span>
          </div>

          {/* Monitoring Status */}
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${orchestratorRunning ? 'bg-emerald-400 animate-pulse' : 'bg-red-400'}`} />
            <span className="text-xs text-slate-400">
              {orchestratorRunning ? 'Live' : 'Paused'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
