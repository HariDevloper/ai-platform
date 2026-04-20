import { useEffect } from 'react'
import { useThemeStore } from '../store/themeStore'

export const useTheme = () => {
  const { mode, setMode, toggleMode } = useThemeStore()

  useEffect(() => {
    document.documentElement.classList.toggle('dark', mode === 'dark')
  }, [mode])

  return { mode, setMode, toggleMode }
}
