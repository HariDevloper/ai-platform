import { useMemo } from 'react'

export const useFilePreview = (file?: File) => {
  return useMemo(() => {
    if (!file) return { type: 'none' as const, preview: [] as string[] }

    if (file.type.startsWith('image/')) {
      return { type: 'image' as const, preview: [URL.createObjectURL(file)] }
    }

    if (file.type.includes('csv') || file.name.endsWith('.csv')) {
      return { type: 'csv' as const, preview: ['CSV preview will be generated after parsing.'] }
    }

    return { type: 'text' as const, preview: ['Text preview available after upload.'] }
  }, [file])
}
