import type { PropsWithChildren } from 'react'
import { cn } from '../../utils/cn'

export const Card = ({ children, className }: PropsWithChildren<{ className?: string }>) => (
  <div className={cn('rounded-2xl bg-white p-5 shadow-soft dark:bg-slate-900', className)}>{children}</div>
)

export const CardTitle = ({ children }: PropsWithChildren) => (
  <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-300">{children}</h3>
)
