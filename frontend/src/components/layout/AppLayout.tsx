import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar'
import { TopNavbar } from './TopNavbar'

export const AppLayout = () => (
  <div className="min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100 md:flex">
    <Sidebar />
    <div className="flex-1">
      <TopNavbar />
      <main className="p-4 md:p-6">
        <Outlet />
      </main>
    </div>
  </div>
)
