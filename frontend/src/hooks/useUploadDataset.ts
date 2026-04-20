import { useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import { uploadDataset } from '../services/evaluationService'
import { useDatasetsStore } from '../store/datasetsStore'
import type { UploadDatasetFormData } from '../types/api'

export const useUploadDataset = () => {
  const [progress, setProgress] = useState(0)
  const addDataset = useDatasetsStore((state) => state.addDataset)

  const mutation = useMutation({
    mutationFn: (data: UploadDatasetFormData) => uploadDataset(data, setProgress),
    onSuccess: (dataset) => {
      addDataset(dataset)
      setProgress(100)
    },
    onError: () => {
      setProgress(0)
    },
  })

  return { ...mutation, progress }
}
