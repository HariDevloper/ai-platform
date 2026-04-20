import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { ChartWrapper } from '../../components/charts/ChartWrapper'
import { ConfusionMatrixHeatmap } from '../../components/charts/ConfusionMatrixHeatmap'
import { FeatureImportanceChart } from '../../components/charts/FeatureImportanceChart'
import { MetricCard } from '../../components/charts/MetricCard'
import { RobustnessChart } from '../../components/charts/RobustnessChart'
import { Button } from '../../components/ui/Button'
import { Card } from '../../components/ui/Card'

const metricCards = [
  { label: 'Accuracy', value: '94.2%' },
  { label: 'Precision', value: '92.1%' },
  { label: 'Recall', value: '91.4%' },
  { label: 'F1 Score', value: '91.7%' },
]

const trendData = [
  { run: 'Run 1', accuracy: 0.86, f1: 0.83 },
  { run: 'Run 2', accuracy: 0.89, f1: 0.86 },
  { run: 'Run 3', accuracy: 0.91, f1: 0.89 },
  { run: 'Run 4', accuracy: 0.94, f1: 0.917 },
]

const performanceBars = [
  { metric: 'Accuracy', value: 94.2 },
  { metric: 'Precision', value: 92.1 },
  { metric: 'Recall', value: 91.4 },
  { metric: 'F1', value: 91.7 },
]

const confusion = [
  [234, 12, 4],
  [10, 198, 8],
  [3, 9, 245],
]

const biasData = [
  { group: 'Group A', score: 0.93 },
  { group: 'Group B', score: 0.89 },
  { group: 'Group C', score: 0.9 },
]

const featureData = [
  { feature: 'income', importance: 0.31 },
  { feature: 'age', importance: 0.25 },
  { feature: 'history', importance: 0.19 },
  { feature: 'location', importance: 0.15 },
]

const robustnessData = [
  { test: 'Gaussian noise', score: 0.87 },
  { test: 'Uniform noise', score: 0.84 },
  { test: 'Dropout perturb', score: 0.8 },
]

export const ResultsPage = () => (
  <div className="space-y-6">
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {metricCards.map((metric) => (
        <MetricCard key={metric.label} label={metric.label} value={metric.value} />
      ))}
    </div>

    <div className="grid gap-4 xl:grid-cols-2">
      <ChartWrapper title="Metric trends">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={trendData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="run" />
            <YAxis domain={[0.7, 1]} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="accuracy" stroke="#2563eb" strokeWidth={2} />
            <Line type="monotone" dataKey="f1" stroke="#14b8a6" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </ChartWrapper>

      <ChartWrapper title="Performance breakdown">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={performanceBars}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="metric" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#3b82f6" radius={6} />
          </BarChart>
        </ResponsiveContainer>
      </ChartWrapper>
    </div>

    <div className="grid gap-4 xl:grid-cols-2">
      <ChartWrapper title="Confusion matrix">
        <ConfusionMatrixHeatmap matrix={confusion} />
      </ChartWrapper>

      <ChartWrapper title="Bias analysis">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={biasData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="group" />
            <YAxis domain={[0, 1]} />
            <Tooltip />
            <Bar dataKey="score" fill="#8b5cf6" radius={6} />
          </BarChart>
        </ResponsiveContainer>
      </ChartWrapper>
    </div>

    <div className="grid gap-4 xl:grid-cols-2">
      <ChartWrapper title="Explainability - feature importance">
        <FeatureImportanceChart data={featureData} />
      </ChartWrapper>

      <ChartWrapper title="Robustness testing">
        <RobustnessChart data={robustnessData} />
      </ChartWrapper>
    </div>

    <Card className="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h3 className="font-semibold">Export & Share</h3>
        <p className="text-sm text-slate-500 dark:text-slate-300">Download evaluation report or share result snapshot.</p>
      </div>
      <div className="flex gap-2">
        <Button variant="secondary">Share results</Button>
        <Button onClick={() => window.print()}>Download report</Button>
      </div>
    </Card>
  </div>
)
