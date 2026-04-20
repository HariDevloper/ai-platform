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

interface ApiEnvelope<T> {
  success: boolean
  data: T
  message: string
  error?: string
}

const unwrap = <T>(payload: ApiEnvelope<T>): T => {
  if (!payload.success) {
    throw new Error(payload.error || payload.message || 'Request failed')
  }
  return payload.data
}

export const uploadModel = async (
  payload: UploadModelFormData,
  onUploadProgress?: (progress: number) => void,
): Promise<ModelItem> => {
  const formData = new FormData()
  formData.append('name', payload.name)
  formData.append('framework', payload.framework)
  formData.append('model_type', payload.model_type)
  formData.append('file', payload.file)

  const { data } = await api.post<ApiEnvelope<ModelItem>>('/api/models/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (event: AxiosProgressEvent) => {
      if (!event.total) return
      onUploadProgress?.(Math.round((event.loaded * 100) / event.total))
    },
  })

  return unwrap(data)
}

export const uploadDataset = async (
  payload: UploadDatasetFormData,
  onUploadProgress?: (progress: number) => void,
): Promise<DatasetItem> => {
  const formData = new FormData()
  formData.append('name', payload.name)
  formData.append('dataset_type', payload.dataset_type)
  formData.append('file', payload.file)

  const { data } = await api.post<ApiEnvelope<DatasetItem>>('/api/datasets/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (event: AxiosProgressEvent) => {
      if (!event.total) return
      onUploadProgress?.(Math.round((event.loaded * 100) / event.total))
    },
  })

  return unwrap(data)
}

export const createEvaluation = async (payload: EvaluateRequest) => {
  const { data } = await api.post<ApiEnvelope<EvaluationItem>>('/api/evaluations/create', payload)
  return unwrap(data)
}

export const fetchEvaluations = async () => {
  const { data } = await api.get<ApiEnvelope<EvaluationItem[]>>('/api/evaluations')
  return unwrap(data)
}

export const fetchResultById = async (id: number) => {
  const { data } = await api.get<ApiEnvelope<EvaluationResult>>(`/api/evaluations/${id}/results`)
  return unwrap(data)
}
