import type { ButtonHTMLAttributes, PropsWithChildren } from 'react'
import { cn } from '../../utils/cn'

type Variant = 'primary' | 'secondary' | 'danger'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
}

const variantClass: Record<Variant, string> = {
  primary: 'bg-brand-600 text-white hover:bg-brand-500',
  secondary: 'bg-slate-100 text-slate-900 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700',
  danger: 'bg-rose-600 text-white hover:bg-rose-500',
}

export const Button = ({ variant = 'primary', className, children, ...props }: PropsWithChildren<ButtonProps>) => (
  <button
    className={cn(
      'inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-semibold transition-all focus:outline-none focus:ring-2 focus:ring-brand-400 disabled:cursor-not-allowed disabled:opacity-50',
      variantClass[variant],
      className,
    )}
    {...props}
  >
    {children}
  </button>
)
