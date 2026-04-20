import { useMemo, useState } from 'react'

interface Column<T> {
  key: keyof T
  title: string
}

export const Table = <T extends Record<string, string | number | undefined>>({
  columns,
  data,
}: {
  columns: Column<T>[]
  data: T[]
}) => {
  const [sortBy, setSortBy] = useState<keyof T | null>(null)
  const [query, setQuery] = useState('')

  const filtered = useMemo(() => {
    const source = data.filter((row) =>
      Object.values(row)
        .join(' ')
        .toLowerCase()
        .includes(query.toLowerCase()),
    )
    if (!sortBy) return source
    return [...source].sort((a, b) => String(a[sortBy]).localeCompare(String(b[sortBy])))
  }, [data, query, sortBy])

  return (
    <div className="space-y-3">
      <input
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder="Filter..."
        className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm dark:border-slate-700 dark:bg-slate-950"
      />
      <div className="overflow-x-auto rounded-2xl border border-slate-200 dark:border-slate-700">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-slate-50 dark:bg-slate-800">
            <tr>
              {columns.map((column) => (
                <th key={String(column.key)} className="px-4 py-3 font-semibold">
                  <button onClick={() => setSortBy(column.key)}>{column.title}</button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((row, rowIndex) => (
              <tr key={rowIndex} className="border-t border-slate-200 dark:border-slate-700">
                {columns.map((column) => (
                  <td key={String(column.key)} className="px-4 py-3">
                    {row[column.key] ?? '-'}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
