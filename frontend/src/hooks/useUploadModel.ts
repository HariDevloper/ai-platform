import { useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import { uploadModel } from '../services/evaluationService'
import { useModelsStore } from '../store/modelsStore'
import type { UploadModelFormData } from '../types/api'

export const useUploadModel = () => {
  const [progress, setProgress] = useState(0)
  const addModel = useModelsStore((state) => state.addModel)

  const mutation = useMutation({
    mutationFn: (data: UploadModelFormData) => uploadModel(data, setProgress),
    onSuccess: (model) => {
      addModel(model)
      setProgress(100)
    },
    onError: () => {
      setProgress(0)
    },
  })

  return { ...mutation, progress }
}
