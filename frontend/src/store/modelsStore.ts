import { create } from 'zustand'
import type { ModelItem } from '../types/api'

interface ModelsState {
  models: ModelItem[]
  selectedModel?: number
  setModels: (models: ModelItem[]) => void
  addModel: (model: ModelItem) => void
  setSelectedModel: (id?: number) => void
}

export const useModelsStore = create<ModelsState>((set) => ({
  models: [],
  selectedModel: undefined,
  setModels: (models) => set({ models }),
  addModel: (model) => set((state) => ({ models: [model, ...state.models] })),
  setSelectedModel: (id) => set({ selectedModel: id }),
}))
