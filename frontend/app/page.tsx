'use client'

import { useState } from 'react'
import { ConfigForm } from '@/components/config-form'
import { ExperimentRunner } from '@/components/experiment-runner'

type Config = {
  numTurns: number
  numSamples: number
  modelName: string
  agents: { name: string; systemPrompt: string }[]
}

export default function Home() {
  const [config, setConfig] = useState<Config | null>(null)
  const [isRunning, setIsRunning] = useState(false)

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-accent/5">
      <div className="container mx-auto px-6 py-12">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold tracking-tight text-foreground mb-4">
              Claude Agent Experiments
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Configure and run multi-agent conversations with Claude. Design experiments, 
              watch conversations unfold in real-time, and analyze the results.
            </p>
          </div>

          {!config ? (
            <ConfigForm onSubmit={setConfig} />
          ) : (
            <ExperimentRunner 
              config={config} 
              onReset={() => setConfig(null)}
              isRunning={isRunning}
              setIsRunning={setIsRunning}
            />
          )}
        </div>
      </div>
    </div>
  )
}
