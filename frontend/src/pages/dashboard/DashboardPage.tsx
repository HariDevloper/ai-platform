import { Card } from '../../components/ui/Card'
import { Table } from '../../components/ui/Table'

const overview = [
  { label: 'Total Models', value: 12 },
  { label: 'Total Datasets', value: 9 },
  { label: 'Evaluations', value: 41 },
]

const recent = [
  { id: 1201, status: 'completed', model: 'FraudNet-v2', score: 0.93 },
  { id: 1202, status: 'running', model: 'Vision-R101', score: 0.0 },
]

export const DashboardPage = () => (
  <div className="space-y-6">
    <div className="grid gap-4 md:grid-cols-3">
      {overview.map((item) => (
        <Card key={item.label}>
          <p className="text-sm text-slate-500 dark:text-slate-300">{item.label}</p>
          <p className="mt-2 text-2xl font-bold">{item.value}</p>
        </Card>
      ))}
    </div>
    <Card>
      <h2 className="mb-4 text-lg font-semibold">Recent evaluations</h2>
      <Table columns={[{ key: 'id', title: 'ID' }, { key: 'model', title: 'Model' }, { key: 'status', title: 'Status' }, { key: 'score', title: 'Score' }]} data={recent} />
    </Card>
  </div>
)
