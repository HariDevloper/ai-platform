import { Suspense, lazy } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import { AppLayout } from './components/layout/AppLayout'
import { ErrorBoundary } from './components/ui/ErrorBoundary'
import { Spinner } from './components/ui/Spinner'
import { useTheme } from './hooks/useTheme'

const DashboardPage = lazy(() => import('./pages/dashboard/DashboardPage').then((module) => ({ default: module.DashboardPage })))
const ModelsPage = lazy(() => import('./pages/models/ModelsPage').then((module) => ({ default: module.ModelsPage })))
const DatasetsPage = lazy(() => import('./pages/datasets/DatasetsPage').then((module) => ({ default: module.DatasetsPage })))
const EvaluatePage = lazy(() => import('./pages/evaluate/EvaluatePage').then((module) => ({ default: module.EvaluatePage })))
const EvaluationStatusPage = lazy(() =>
  import('./pages/status/EvaluationStatusPage').then((module) => ({ default: module.EvaluationStatusPage })),
)
const ResultsPage = lazy(() => import('./pages/results/ResultsPage').then((module) => ({ default: module.ResultsPage })))

const App = () => {
  useTheme()

  return (
    <ErrorBoundary>
      <Suspense fallback={<div className="flex min-h-[40vh] items-center justify-center"><Spinner /></div>}>
        <Routes>
          <Route element={<AppLayout />}>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/models" element={<ModelsPage />} />
            <Route path="/datasets" element={<DatasetsPage />} />
            <Route path="/evaluate" element={<EvaluatePage />} />
            <Route path="/status" element={<EvaluationStatusPage />} />
            <Route path="/results" element={<ResultsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </Suspense>
    </ErrorBoundary>
  )
}

export default App
