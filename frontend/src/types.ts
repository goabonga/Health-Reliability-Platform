export interface HealthSignal {
  timestamp: string;
  sleep_hours: number;
  steps: number;
  stress_score: number;
  heart_rate_rest: number;
}

export interface SLOResult {
  slo_name: string;
  metric: string;
  current_value: number;
  threshold: number;
  operator: string;
  passed: boolean;
}

export interface Incident {
  id: string;
  timestamp: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  source: string;
  status: 'open' | 'mitigated' | 'resolved';
}

export interface Action {
  id: string;
  timestamp: string;
  incident_id: string;
  action_type: string;
  description: string;
  agent: string;
}

export interface TimelineEvent {
  timestamp: string;
  event_type: 'signal' | 'slo' | 'agent' | 'action' | 'incident' | 'system';
  message: string;
  details?: Record<string, unknown>;
}

export interface SystemState {
  latest_signal: HealthSignal | null;
  total_signals: number;
  open_incidents: Incident[];
  total_incidents: number;
  recent_actions: Action[];
  total_actions: number;
}
