import { Card } from '../ui/Card'

export const MetricCard = ({ label, value }: { label: string; value: string }) => (
  <Card>
    <p className="text-sm text-slate-500 dark:text-slate-300">{label}</p>
    <p className="mt-2 text-2xl font-bold">{value}</p>
  </Card>
)
