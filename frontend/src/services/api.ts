import axios, { AxiosError, type InternalAxiosRequestConfig } from 'axios'

interface RetryableRequestConfig extends InternalAxiosRequestConfig {
  _retryCount?: number
}

const MAX_RETRIES = 2
const RETRY_DELAY_MS = 500

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
  timeout: 30_000,
})

api.interceptors.request.use((config) => {
  config.headers.set('Accept', 'application/json')
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const config = error.config as RetryableRequestConfig | undefined

    if (config && (!error.response || error.response.status >= 500)) {
      config._retryCount = (config._retryCount ?? 0) + 1
      if (config._retryCount <= MAX_RETRIES) {
        await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY_MS * config._retryCount!))
        return api.request(config)
      }
    }

    const message =
      (error.response?.data as { detail?: string } | undefined)?.detail ??
      error.message ??
      'Unexpected server error'

    return Promise.reject(new Error(message))
  },
)
