import type { EvaluationStatus } from '../../types/api'

const colors: Record<EvaluationStatus, string> = {
  pending: 'bg-amber-100 text-amber-700',
  running: 'bg-blue-100 text-blue-700',
  completed: 'bg-emerald-100 text-emerald-700',
  failed: 'bg-rose-100 text-rose-700',
  cancelled: 'bg-slate-200 text-slate-700',
}

export const EvaluationStatusBadge = ({ status }: { status: EvaluationStatus }) => (
  <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${colors[status]}`}>{status}</span>
)
