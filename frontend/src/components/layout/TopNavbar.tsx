import { useTheme } from '../../hooks/useTheme'
import { Button } from '../ui/Button'

export const TopNavbar = () => {
  const { mode, toggleMode } = useTheme()

  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-4 dark:border-slate-800 dark:bg-slate-900">
      <p className="text-sm text-slate-500 dark:text-slate-300">AI Model Evaluation Workspace</p>
      <div className="flex items-center gap-2">
        <Button variant="secondary" onClick={toggleMode}>
          {mode === 'dark' ? 'Light' : 'Dark'} mode
        </Button>
        <Button variant="secondary">User</Button>
      </div>
    </header>
  )
}
