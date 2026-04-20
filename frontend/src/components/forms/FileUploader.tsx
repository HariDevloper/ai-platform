import { useRef, useState } from 'react'
import { Button } from '../ui/Button'

interface FileUploaderProps {
  accept?: string
  maxSizeMb?: number
  onFileSelect: (file: File) => void
  progress?: number
}

export const FileUploader = ({ accept, maxSizeMb = 50, onFileSelect, progress = 0 }: FileUploaderProps) => {
  const [error, setError] = useState<string>()
  const inputRef = useRef<HTMLInputElement | null>(null)

  const handleFile = (file?: File) => {
    if (!file) return
    if (file.size > maxSizeMb * 1024 * 1024) {
      setError(`File must be smaller than ${maxSizeMb}MB`)
      return
    }
    setError(undefined)
    onFileSelect(file)
  }

  return (
    <div className="space-y-3">
      <div
        className="cursor-pointer rounded-2xl border-2 border-dashed border-slate-300 p-6 text-center transition hover:border-brand-400 dark:border-slate-700"
        onDrop={(event) => {
          event.preventDefault()
          handleFile(event.dataTransfer.files[0])
        }}
        onDragOver={(event) => event.preventDefault()}
        onClick={() => inputRef.current?.click()}
      >
        <p className="text-sm text-slate-500 dark:text-slate-300">Drag & drop file here, or click to upload</p>
        <input
          ref={inputRef}
          type="file"
          className="hidden"
          accept={accept}
          onChange={(event) => handleFile(event.target.files?.[0])}
        />
      </div>
      {progress > 0 ? (
        <div className="h-2 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-800">
          <div className="h-full rounded-full bg-brand-600 transition-all" style={{ width: `${progress}%` }} />
        </div>
      ) : null}
      {error ? <p className="text-sm text-rose-600">{error}</p> : null}
      <Button type="button" variant="secondary" onClick={() => inputRef.current?.click()}>
        Browse file
      </Button>
    </div>
  )
}
