import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

export const FeatureImportanceChart = ({ data }: { data: Array<{ feature: string; importance: number }> }) => (
  <ResponsiveContainer width="100%" height="100%">
    <BarChart data={data} layout="vertical" margin={{ left: 24 }}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis type="number" />
      <YAxis dataKey="feature" type="category" width={100} />
      <Tooltip />
      <Bar dataKey="importance" fill="#2563eb" radius={6} />
    </BarChart>
  </ResponsiveContainer>
)
