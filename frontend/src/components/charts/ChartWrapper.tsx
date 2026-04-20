import type { PropsWithChildren } from 'react'
import { Card, CardTitle } from '../ui/Card'

export const ChartWrapper = ({ title, children }: PropsWithChildren<{ title: string }>) => (
  <Card>
    <CardTitle>{title}</CardTitle>
    <div className="mt-4 h-72">{children}</div>
  </Card>
)
