import type { PropsWithChildren } from 'react'
import { cn } from '../../utils/cn'

interface TabsProps {
  activeTab: string
  onChange: (tab: string) => void
  tabs: string[]
}

export const Tabs = ({ activeTab, onChange, tabs }: TabsProps) => (
  <div className="flex flex-wrap gap-2">
    {tabs.map((tab) => (
      <button
        key={tab}
        onClick={() => onChange(tab)}
        className={cn(
          'rounded-xl px-3 py-1.5 text-sm transition',
          activeTab === tab
            ? 'bg-brand-600 text-white'
            : 'bg-slate-100 text-slate-600 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700',
        )}
      >
        {tab}
      </button>
    ))}
  </div>
)

export const TabPanel = ({ children }: PropsWithChildren) => <div className="pt-4">{children}</div>
