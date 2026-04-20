import { useCallback } from 'react'

export const useLocalStorage = <T>(key: string, initialValue: T) => {
  const getValue = useCallback((): T => {
    const raw = localStorage.getItem(key)
    if (!raw) return initialValue
    try {
      return JSON.parse(raw) as T
    } catch {
      return initialValue
    }
  }, [initialValue, key])

  const setValue = useCallback(
    (value: T) => {
      localStorage.setItem(key, JSON.stringify(value))
    },
    [key],
  )

  return { getValue, setValue }
}
