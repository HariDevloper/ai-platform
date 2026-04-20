import { AnimatePresence, motion } from 'framer-motion'
import type { PropsWithChildren } from 'react'

interface ModalProps {
  open: boolean
  onClose: () => void
  title: string
}

export const Modal = ({ open, onClose, title, children }: PropsWithChildren<ModalProps>) => (
  <AnimatePresence>
    {open ? (
      <motion.div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
        <motion.div className="w-full max-w-lg rounded-2xl bg-white p-6 dark:bg-slate-900" initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} exit={{ y: 20, opacity: 0 }}>
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-lg font-semibold">{title}</h3>
            <button onClick={onClose} className="text-slate-500">✕</button>
          </div>
          {children}
        </motion.div>
      </motion.div>
    ) : null}
  </AnimatePresence>
)
