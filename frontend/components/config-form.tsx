'use client'

import { useState } from 'react'
import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Plus, Trash2, Settings, Users, Play } from 'lucide-react'
import ModelsDropdown from './models-dropdown'

const configSchema = z.object({
  numTurns: z.number().min(1).max(50),
  numSamples: z.number().min(1).max(10),
  modelName: z.string().min(1),
  agents: z.array(z.object({
    name: z.string().min(1),
    systemPrompt: z.string().min(1)
  })).min(1).max(10)
})

type ConfigForm = z.infer<typeof configSchema>

interface ConfigFormProps {
  onSubmit: (config: ConfigForm) => void
}

export function ConfigForm({ onSubmit }: ConfigFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)

  const { register, control, handleSubmit, watch, setValue, formState: { errors } } = useForm<ConfigForm>({
    resolver: zodResolver(configSchema),
    defaultValues: {
      numTurns: 5,
      numSamples: 1,
      modelName: 'claude-sonnet-4-20250514',
      agents: [
        { name: 'Claude 1', systemPrompt: 'You are a helpful AI talking with another helpful AI' },
        { name: 'Claude 2', systemPrompt: 'You are a helpful AI talking with another helpful AI' }
      ]
    }
  })

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'agents'
  })

  const modelName = watch('modelName')

  const onFormSubmit = async (data: ConfigForm) => {
    setIsSubmitting(true)
    try {
      onSubmit(data)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Card className="backdrop-blur-sm bg-card/50 border-border/50 shadow-2xl">
      <CardHeader className="text-center pb-8">
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center">
          <Settings className="w-8 h-8 text-primary" />
        </div>
        <CardTitle className="text-2xl font-semibold">Experiment Configuration</CardTitle>
        <CardDescription className="text-base">
          Set up your multi-agent conversation parameters and agent behaviors
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-8">
        <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <Label htmlFor="numTurns" className="text-sm font-medium">
                Number of Turns
              </Label>
              <Input
                id="numTurns"
                type="number"
                min="1"
                max="50"
                className="bg-background/50"
                {...register('numTurns', { valueAsNumber: true })}
              />
              {errors.numTurns && (
                <p className="text-sm text-destructive">{errors.numTurns.message}</p>
              )}
            </div>

            {/*  <div className="space-y-2">
              <Label htmlFor="numSamples" className="text-sm font-medium">
                Number of Samples
              </Label>
              <Input
                id="numSamples"
                type="number"
                min="1"
                max="10"
                className="bg-background/50"
                {...register('numSamples', { valueAsNumber: true })}
              />
              {errors.numSamples && (
                <p className="text-sm text-destructive">{errors.numSamples.message}</p>
              )}
            </div> */}

            <div className="space-y-2">
              <Label htmlFor="modelName" className="text-sm font-medium">
                Model Name
              </Label>
              <ModelsDropdown
                value={modelName}
                onChange={(value) => setValue('modelName', value)}
              />
              {errors.modelName && (
                <p className="text-sm text-destructive">{errors.modelName.message}</p>
              )}
            </div>
          </div>

          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Users className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold">Agents</h3>
              </div>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => append({ name: '', systemPrompt: '' })}
                className="gap-2"
              >
                <Plus className="w-4 h-4" />
                Add Agent
              </Button>
            </div>

            <div className="grid gap-6">
              {fields.map((field, index) => (
                <Card key={field.id} className="border-border/30 bg-muted/20">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                    <CardTitle className="text-base">Agent {index + 1}</CardTitle>
                    {fields.length > 1 && (
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => remove(index)}
                        className="text-destructive hover:text-destructive/80"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    )}
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor={`agents.${index}.name`} className="text-sm font-medium">
                        Name
                      </Label>
                      <Input
                        id={`agents.${index}.name`}
                        placeholder="e.g., Claude Assistant"
                        className="bg-background/50"
                        {...register(`agents.${index}.name`)}
                      />
                      {errors.agents?.[index]?.name && (
                        <p className="text-sm text-destructive">
                          {errors.agents[index]?.name?.message}
                        </p>
                      )}
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor={`agents.${index}.systemPrompt`} className="text-sm font-medium">
                        System Prompt
                      </Label>
                      <Textarea
                        id={`agents.${index}.systemPrompt`}
                        placeholder="Define the agent's role, personality, and behavior..."
                        rows={3}
                        className="bg-background/50 resize-none"
                        {...register(`agents.${index}.systemPrompt`)}
                      />
                      {errors.agents?.[index]?.systemPrompt && (
                        <p className="text-sm text-destructive">
                          {errors.agents[index]?.systemPrompt?.message}
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          <div className="flex justify-center pt-6">
            <Button
              type="submit"
              size="lg"
              disabled={isSubmitting}
              className="min-w-48 gap-2 bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 shadow-lg"
            >
              {isSubmitting ? (
                <div className="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin" />
              ) : (
                <Play className="w-5 h-5" />
              )}
              {isSubmitting ? 'Starting Experiment...' : 'Next'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}