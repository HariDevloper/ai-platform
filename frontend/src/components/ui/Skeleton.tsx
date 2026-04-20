export const Skeleton = ({ className = 'h-6 w-full' }: { className?: string }) => (
  <div className={`animate-pulse rounded-xl bg-slate-200 dark:bg-slate-700 ${className}`} />
)
