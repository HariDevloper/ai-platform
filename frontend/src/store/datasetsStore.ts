import { create } from 'zustand'
import type { DatasetItem } from '../types/api'

interface DatasetsState {
  datasets: DatasetItem[]
  selectedDataset?: number
  setDatasets: (datasets: DatasetItem[]) => void
  addDataset: (dataset: DatasetItem) => void
  setSelectedDataset: (id?: number) => void
}

export const useDatasetsStore = create<DatasetsState>((set) => ({
  datasets: [],
  selectedDataset: undefined,
  setDatasets: (datasets) => set({ datasets }),
  addDataset: (dataset) => set((state) => ({ datasets: [dataset, ...state.datasets] })),
  setSelectedDataset: (id) => set({ selectedDataset: id }),
}))
