import { useQuery } from '@tanstack/react-query'
import { fetchEvaluations } from '../services/evaluationService'

export const useEvaluationStatus = () =>
  useQuery({
    queryKey: ['evaluations'],
    queryFn: fetchEvaluations,
    refetchInterval: 3000,
  })
