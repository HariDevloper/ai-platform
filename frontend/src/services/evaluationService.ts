import type { AxiosProgressEvent } from 'axios'
import { api } from './api'
import type {
  DatasetItem,
  EvaluateRequest,
  EvaluationItem,
  EvaluationResult,
  ModelItem,
  UploadDatasetFormData,
  UploadModelFormData,
} from '../types/api'

export const uploadModel = async (
  payload: UploadModelFormData,
  onUploadProgress?: (progress: number) => void,
): Promise<ModelItem> => {
  const formData = new FormData()
  formData.append('name', payload.name)
  formData.append('framework', payload.framework)
  formData.append('model_type', payload.model_type)
  formData.append('file', payload.file)

  const { data } = await api.post<ModelItem>('/models/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (event: AxiosProgressEvent) => {
      if (!event.total) return
      onUploadProgress?.(Math.round((event.loaded * 100) / event.total))
    },
  })

  return data
}

export const uploadDataset = async (
  payload: UploadDatasetFormData,
  onUploadProgress?: (progress: number) => void,
): Promise<DatasetItem> => {
  const formData = new FormData()
  formData.append('name', payload.name)
  formData.append('dataset_type', payload.dataset_type)
  formData.append('file', payload.file)

  const { data } = await api.post<DatasetItem>('/datasets/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (event: AxiosProgressEvent) => {
      if (!event.total) return
      onUploadProgress?.(Math.round((event.loaded * 100) / event.total))
    },
  })

  return data
}

export const createEvaluation = async (payload: EvaluateRequest) => {
  const { data } = await api.post<EvaluationItem>('/evaluate', payload)
  return data
}

export const fetchEvaluations = async () => {
  const { data } = await api.get<EvaluationItem[]>('/evaluations')
  return data
}

export const fetchResultById = async (id: number) => {
  const { data } = await api.get<EvaluationResult>(`/results/${id}`)
  return data
}
