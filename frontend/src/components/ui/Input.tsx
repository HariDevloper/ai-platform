import type { InputHTMLAttributes } from 'react'
import { cn } from '../../utils/cn'

export const Input = ({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) => (
  <input
    className={cn(
      'w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none transition focus:border-brand-500 dark:border-slate-700 dark:bg-slate-950',
      className,
    )}
    {...props}
  />
)
