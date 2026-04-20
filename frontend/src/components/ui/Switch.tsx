interface SwitchProps {
  checked: boolean
  onChange: (checked: boolean) => void
}

export const Switch = ({ checked, onChange }: SwitchProps) => (
  <button
    type="button"
    onClick={() => onChange(!checked)}
    className={`relative h-6 w-11 rounded-full transition ${checked ? 'bg-brand-600' : 'bg-slate-300 dark:bg-slate-700'}`}
  >
    <span
      className={`absolute top-0.5 h-5 w-5 rounded-full bg-white transition ${checked ? 'left-5' : 'left-0.5'}`}
    />
  </button>
)
