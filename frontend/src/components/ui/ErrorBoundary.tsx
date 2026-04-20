import { Component, type PropsWithChildren } from 'react'

interface ErrorBoundaryState {
  hasError: boolean
}

export class ErrorBoundary extends Component<PropsWithChildren, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  render() {
    if (this.state.hasError) {
      return <div className="rounded-2xl bg-rose-50 p-6 text-rose-700">Something went wrong while rendering this page.</div>
    }

    return this.props.children
  }
}
