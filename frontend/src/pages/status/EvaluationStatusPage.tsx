import { EvaluationStatusBadge } from '../../components/charts/EvaluationStatusBadge'
import { Card } from '../../components/ui/Card'
import { Skeleton } from '../../components/ui/Skeleton'
import { useEvaluationStatus } from '../../hooks/useEvaluationStatus'

export const EvaluationStatusPage = () => {
  const { data, isLoading } = useEvaluationStatus()

  if (isLoading) {
    return (
      <div className="space-y-3">
        <Skeleton className="h-12 w-full" />
        <Skeleton className="h-12 w-full" />
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {(data ?? []).map((evaluation) => (
        <Card key={evaluation.id} className="flex items-center justify-between">
          <div>
            <p className="font-semibold">Evaluation #{evaluation.id}</p>
            <p className="text-xs text-slate-500 dark:text-slate-300">Created {new Date(evaluation.created_at).toLocaleString()}</p>
          </div>
          <EvaluationStatusBadge status={evaluation.status} />
        </Card>
      ))}
    </div>
  )
}
