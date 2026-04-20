import { createContext } from 'react'

type ToastType = 'success' | 'error' | 'info'

export interface ToastContextValue {
  pushToast: (message: string, type?: ToastType) => void
}

export const ToastContext = createContext<ToastContextValue | null>(null)
export type { ToastType }
