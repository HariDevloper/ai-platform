import { zodResolver } from '@hookform/resolvers/zod'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { FileUploader } from '../../components/forms/FileUploader'
import { Button } from '../../components/ui/Button'
import { Card } from '../../components/ui/Card'
import { Input } from '../../components/ui/Input'
import { Select } from '../../components/ui/Select'
import { useUploadModel } from '../../hooks/useUploadModel'
import { useToast } from '../../hooks/useToast'

const schema = z.object({
  name: z.string().min(2, 'Name is required'),
  framework: z.enum(['pytorch', 'tensorflow', 'sklearn', 'custom_api', 'onnx']),
  model_type: z.enum(['classification', 'regression', 'nlp', 'vision', 'custom']),
})

type FormValues = z.infer<typeof schema>

export const ModelsPage = () => {
  const [selectedFile, setSelectedFile] = useState<File>()
  const { register, handleSubmit, formState } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { framework: 'pytorch', model_type: 'classification' },
  })
  const { mutateAsync, progress, isPending } = useUploadModel()
  const { pushToast } = useToast()

  return (
    <Card className="max-w-2xl space-y-4">
      <h2 className="text-lg font-semibold">Upload model</h2>
      <form
        className="space-y-4"
        onSubmit={handleSubmit(async (values) => {
          if (!selectedFile) {
            pushToast('Please attach a model file', 'error')
            return
          }
          await mutateAsync({ ...values, file: selectedFile })
          pushToast('Model uploaded successfully', 'success')
        })}
      >
        <Input placeholder="Model name" {...register('name')} />
        <Select {...register('framework')}>
          <option value="pytorch">PyTorch</option>
          <option value="tensorflow">TensorFlow</option>
          <option value="sklearn">Scikit-learn</option>
          <option value="custom_api">Custom API</option>
          <option value="onnx">ONNX</option>
        </Select>
        <Select {...register('model_type')}>
          <option value="classification">Classification</option>
          <option value="regression">Regression</option>
          <option value="nlp">NLP</option>
          <option value="vision">Vision</option>
          <option value="custom">Custom</option>
        </Select>
        <FileUploader onFileSelect={setSelectedFile} progress={progress} />
        {formState.errors.name ? <p className="text-sm text-rose-600">{formState.errors.name.message}</p> : null}
        <Button type="submit" disabled={isPending}>{isPending ? 'Uploading...' : 'Upload model'}</Button>
      </form>
    </Card>
  )
}
