const palette = ['bg-slate-100', 'bg-brand-200', 'bg-brand-400', 'bg-brand-600']

export const ConfusionMatrixHeatmap = ({ matrix }: { matrix: number[][] }) => {
  const max = Math.max(...matrix.flat())

  return (
    <div className="grid grid-cols-3 gap-2">
      {matrix.flat().map((value, index) => {
        const level = Math.min(palette.length - 1, Math.floor((value / max) * palette.length))
        return (
          <div key={index} className={`rounded-xl p-4 text-center text-sm font-semibold text-slate-900 ${palette[level]}`}>
            {value}
          </div>
        )
      })}
    </div>
  )
}
