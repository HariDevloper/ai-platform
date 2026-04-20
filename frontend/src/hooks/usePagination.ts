import { useMemo, useState } from 'react'

export const usePagination = <T>(items: T[], pageSize = 5) => {
  const [page, setPage] = useState(1)
  const maxPage = Math.max(1, Math.ceil(items.length / pageSize))

  const paginated = useMemo(() => {
    const start = (page - 1) * pageSize
    return items.slice(start, start + pageSize)
  }, [items, page, pageSize])

  return {
    page,
    maxPage,
    setPage,
    paginated,
  }
}
