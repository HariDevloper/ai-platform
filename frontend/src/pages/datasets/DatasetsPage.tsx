import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { FileUploader } from '../../components/forms/FileUploader'
import { Button } from '../../components/ui/Button'
import { Card } from '../../components/ui/Card'
import { Input } from '../../components/ui/Input'
import { Select } from '../../components/ui/Select'
import { useFilePreview } from '../../hooks/useFilePreview'
import { useUploadDataset } from '../../hooks/useUploadDataset'
import { useToast } from '../../hooks/useToast'
import { useState } from 'react'

const schema = z.object({
  name: z.string().min(2, 'Name is required'),
  dataset_type: z.enum(['tabular', 'image', 'text', 'custom']),
})

type FormValues = z.infer<typeof schema>

export const DatasetsPage = () => {
  const [selectedFile, setSelectedFile] = useState<File>()
  const preview = useFilePreview(selectedFile)
  const { register, handleSubmit, formState } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { dataset_type: 'tabular' },
  })
  const { mutateAsync, progress, isPending } = useUploadDataset()
  const { pushToast } = useToast()

  return (
    <Card className="max-w-2xl space-y-4">
      <h2 className="text-lg font-semibold">Upload dataset</h2>
      <form
        className="space-y-4"
        onSubmit={handleSubmit(async (values) => {
          if (!selectedFile) {
            pushToast('Please attach a dataset file', 'error')
            return
          }
          await mutateAsync({ ...values, file: selectedFile })
          pushToast('Dataset uploaded successfully', 'success')
        })}
      >
        <Input placeholder="Dataset name" {...register('name')} />
        <Select {...register('dataset_type')}>
          <option value="tabular">Tabular (CSV)</option>
          <option value="image">Image</option>
          <option value="text">Text</option>
          <option value="custom">Custom</option>
        </Select>
        <FileUploader onFileSelect={setSelectedFile} progress={progress} />

        {preview.type !== 'none' ? (
          <Card className="bg-slate-50 dark:bg-slate-800">
            <p className="mb-2 text-sm font-semibold">Auto preview</p>
            {preview.type === 'image' ? (
              <img src={preview.preview[0]} alt="Dataset preview" className="h-36 rounded-xl object-cover" />
            ) : (
              <p className="text-sm text-slate-500 dark:text-slate-300">{preview.preview[0]}</p>
            )}
            {selectedFile ? (
              <div className="mt-3 text-xs text-slate-500 dark:text-slate-300">
                <p>Size: {(selectedFile.size / 1024).toFixed(2)} KB</p>
                <p>Type: {selectedFile.type || 'unknown'}</p>
              </div>
            ) : null}
          </Card>
        ) : null}

        {formState.errors.name ? <p className="text-sm text-rose-600">{formState.errors.name.message}</p> : null}
        <Button type="submit" disabled={isPending}>{isPending ? 'Uploading...' : 'Upload dataset'}</Button>
      </form>
    </Card>
  )
}
