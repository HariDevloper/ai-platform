export type Framework = 'pytorch' | 'tensorflow' | 'sklearn' | 'custom_api' | 'onnx'
export type ModelTaskType = 'classification' | 'regression' | 'nlp' | 'vision' | 'custom'
export type DatasetType = 'tabular' | 'image' | 'text' | 'custom'
export type EvaluationStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'

export interface ModelItem {
  id: number
  name: string
  framework: Framework
  model_type: ModelTaskType
  created_at: string
}

export interface DatasetItem {
  id: number
  name: string
  dataset_type: DatasetType
  num_samples?: number
  num_features?: number
  created_at: string
}

export interface EvaluateRequest {
  model_id: number
  dataset_id: number
  metrics: string[]
  enable_bias_detection: boolean
  enable_explainability: boolean
  enable_robustness: boolean
}

export interface EvaluationItem {
  id: number
  model_id: number
  dataset_id: number
  status: EvaluationStatus
  created_at: string
  completed_at?: string
}

export interface MetricBundle {
  accuracy?: number
  precision?: number
  recall?: number
  f1_score?: number
  [key: string]: number | undefined
}

export interface EvaluationResult {
  evaluation_id: number
  metrics: MetricBundle
  confusion_matrix?: number[][]
  bias?: Record<string, number>
  explainability?: Array<{ feature: string; importance: number }>
  robustness?: Array<{ test: string; score: number }>
  trust_score?: number
}

export interface UploadModelFormData {
  name: string
  framework: Framework
  model_type: ModelTaskType
  file: File
}

export interface UploadDatasetFormData {
  name: string
  dataset_type: DatasetType
  file: File
}
