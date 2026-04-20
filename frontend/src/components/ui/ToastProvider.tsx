import { useMemo, useState, type PropsWithChildren } from 'react'
import { ToastContext, type ToastType } from './toastContext'

interface ToastItem {
  id: number
  message: string
  type: ToastType
}

export const ToastProvider = ({ children }: PropsWithChildren) => {
  const [toasts, setToasts] = useState<ToastItem[]>([])

  const value = useMemo(
    () => ({
      pushToast: (message: string, type: ToastType = 'info') => {
        const id = Date.now()
        setToasts((current) => [...current, { id, message, type }])
        setTimeout(() => {
          setToasts((current) => current.filter((toast) => toast.id !== id))
        }, 3000)
      },
    }),
    [],
  )

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="fixed right-4 top-4 z-50 space-y-2">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`rounded-xl px-4 py-3 text-sm text-white shadow-soft ${
              toast.type === 'success' ? 'bg-emerald-600' : toast.type === 'error' ? 'bg-rose-600' : 'bg-slate-800'
            }`}
          >
            {toast.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}
