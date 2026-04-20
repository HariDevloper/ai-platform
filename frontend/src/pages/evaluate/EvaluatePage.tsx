import { useEffect } from 'react'
import { Button } from '../../components/ui/Button'
import { Card } from '../../components/ui/Card'
import { Select } from '../../components/ui/Select'
import { Switch } from '../../components/ui/Switch'
import { useEvaluate } from '../../hooks/useEvaluate'
import { useDatasetsStore } from '../../store/datasetsStore'
import { useEvaluationStore } from '../../store/evaluationStore'
import { useModelsStore } from '../../store/modelsStore'
import { useToast } from '../../hooks/useToast'

const availableMetrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']

export const EvaluatePage = () => {
  const models = useModelsStore((state) => state.models)
  const datasets = useDatasetsStore((state) => state.datasets)
  const selectedModel = useModelsStore((state) => state.selectedModel)
  const selectedDataset = useDatasetsStore((state) => state.selectedDataset)
  const setSelectedModel = useModelsStore((state) => state.setSelectedModel)
  const setSelectedDataset = useDatasetsStore((state) => state.setSelectedDataset)
  const config = useEvaluationStore((state) => state.evaluationConfig)
  const setConfig = useEvaluationStore((state) => state.setEvaluationConfig)
  const { mutateAsync, isPending } = useEvaluate()
  const { pushToast } = useToast()

  useEffect(() => {
    if (!selectedModel && models[0]) setSelectedModel(models[0].id)
    if (!selectedDataset && datasets[0]) setSelectedDataset(datasets[0].id)
  }, [datasets, models, selectedDataset, selectedModel, setSelectedDataset, setSelectedModel])

  return (
    <Card className="max-w-3xl space-y-5">
      <h2 className="text-lg font-semibold">Evaluation configuration</h2>

      <div className="grid gap-4 md:grid-cols-2">
        <Select value={selectedModel ?? ''} onChange={(event) => setSelectedModel(Number(event.target.value))}>
          <option value="">Select model</option>
          {models.map((model) => (
            <option key={model.id} value={model.id}>
              {model.name}
            </option>
          ))}
        </Select>
        <Select value={selectedDataset ?? ''} onChange={(event) => setSelectedDataset(Number(event.target.value))}>
          <option value="">Select dataset</option>
          {datasets.map((dataset) => (
            <option key={dataset.id} value={dataset.id}>
              {dataset.name}
            </option>
          ))}
        </Select>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold">Metrics</p>
        <div className="grid gap-2 md:grid-cols-3">
          {availableMetrics.map((metric) => (
            <label key={metric} className="flex items-center gap-2 rounded-xl border border-slate-200 p-2 text-sm dark:border-slate-700">
              <input
                type="checkbox"
                checked={config.metrics.includes(metric)}
                onChange={(event) => {
                  setConfig({
                    metrics: event.target.checked
                      ? [...config.metrics, metric]
                      : config.metrics.filter((value) => value !== metric),
                  })
                }}
              />
              {metric}
            </label>
          ))}
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between"><span>Bias detection</span><Switch checked={config.enable_bias_detection} onChange={(value) => setConfig({ enable_bias_detection: value })} /></div>
        <div className="flex items-center justify-between"><span>Explainability</span><Switch checked={config.enable_explainability} onChange={(value) => setConfig({ enable_explainability: value })} /></div>
        <div className="flex items-center justify-between"><span>Robustness testing</span><Switch checked={config.enable_robustness} onChange={(value) => setConfig({ enable_robustness: value })} /></div>
      </div>

      <Button
        onClick={async () => {
          if (!selectedModel || !selectedDataset) {
            pushToast('Select model and dataset first', 'error')
            return
          }
          await mutateAsync({
            model_id: selectedModel,
            dataset_id: selectedDataset,
            ...config,
          })
          pushToast('Evaluation triggered', 'success')
        }}
        disabled={isPending}
      >
        {isPending ? 'Submitting...' : 'Run evaluation'}
      </Button>
    </Card>
  )
}
