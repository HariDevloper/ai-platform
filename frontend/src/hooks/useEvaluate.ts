import { useMutation } from '@tanstack/react-query'
import { createEvaluation } from '../services/evaluationService'
import type { EvaluateRequest } from '../types/api'

export const useEvaluate = () =>
  useMutation({
    mutationFn: (payload: EvaluateRequest) => createEvaluation(payload),
  })
