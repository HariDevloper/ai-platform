import { create } from 'zustand'
import type { EvaluateRequest, EvaluationResult } from '../types/api'

interface EvaluationState {
  evaluationConfig: Omit<EvaluateRequest, 'model_id' | 'dataset_id'>
  latestResult?: EvaluationResult
  setEvaluationConfig: (config: Partial<Omit<EvaluateRequest, 'model_id' | 'dataset_id'>>) => void
  setLatestResult: (result?: EvaluationResult) => void
}

const defaultConfig: Omit<EvaluateRequest, 'model_id' | 'dataset_id'> = {
  metrics: ['accuracy', 'precision', 'recall', 'f1_score'],
  enable_bias_detection: true,
  enable_explainability: true,
  enable_robustness: true,
}

export const useEvaluationStore = create<EvaluationState>((set) => ({
  evaluationConfig: defaultConfig,
  latestResult: undefined,
  setEvaluationConfig: (config) =>
    set((state) => ({
      evaluationConfig: {
        ...state.evaluationConfig,
        ...config,
      },
    })),
  setLatestResult: (result) => set({ latestResult: result }),
}))
