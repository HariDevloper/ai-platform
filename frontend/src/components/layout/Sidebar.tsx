import { NavLink } from 'react-router-dom'
import { cn } from '../../utils/cn'

const navItems = [
  { to: '/', label: 'Dashboard' },
  { to: '/models', label: 'Models' },
  { to: '/datasets', label: 'Datasets' },
  { to: '/evaluate', label: 'Evaluate' },
  { to: '/status', label: 'Status' },
  { to: '/results', label: 'Results' },
]

export const Sidebar = () => (
  <aside className="w-full border-b border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900 md:w-64 md:border-b-0 md:border-r">
    <h1 className="mb-6 text-lg font-bold">AI Eval Platform</h1>
    <nav className="space-y-1">
      {navItems.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({ isActive }) =>
            cn(
              'block rounded-xl px-3 py-2 text-sm transition',
              isActive
                ? 'bg-brand-600 text-white'
                : 'text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800',
            )
          }
        >
          {item.label}
        </NavLink>
      ))}
    </nav>
  </aside>
)
