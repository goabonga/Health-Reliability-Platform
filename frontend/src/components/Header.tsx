interface HeaderProps {
  orchestratorRunning: boolean;
}

export function Header({ orchestratorRunning }: HeaderProps) {
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
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${orchestratorRunning ? 'bg-emerald-400 animate-pulse' : 'bg-red-400'}`} />
            <span className="text-sm text-slate-300">
              {orchestratorRunning ? 'Monitoring Active' : 'Monitoring Stopped'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
