import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

export const RobustnessChart = ({ data }: { data: Array<{ test: string; score: number }> }) => (
  <ResponsiveContainer width="100%" height="100%">
    <BarChart data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="test" />
      <YAxis domain={[0, 1]} />
      <Tooltip />
      <Bar dataKey="score" fill="#0f766e" radius={6} />
    </BarChart>
  </ResponsiveContainer>
)
