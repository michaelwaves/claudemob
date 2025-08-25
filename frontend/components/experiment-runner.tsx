'use client'

import { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ArrowLeft, Play, Square, Save, X, Users, MessageCircle, Clock } from 'lucide-react'
import { cn } from '@/lib/utils'

type Config = {
  numTurns: number
  numSamples: number
  modelName: string
  agents: { name: string; systemPrompt: string }[]
}

interface Message {
  speaker: string
  content: string
  turn: number
  agent: number
  timestamp: Date
}

interface ExperimentRunnerProps {
  config: Config
  onReset: () => void
  isRunning: boolean
  setIsRunning: (running: boolean) => void
}

export function ExperimentRunner({ config, onReset, isRunning, setIsRunning }: ExperimentRunnerProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [currentTurn, setCurrentTurn] = useState(0)
  const [currentAgent, setCurrentAgent] = useState(0)
  const [conversationHistory, setConversationHistory] = useState<{ role: string; content: string }[]>([])
  const [currentMessage, setCurrentMessage] = useState("Hello! I'm looking forward to our conversation.")
  const [streamingContent, setStreamingContent] = useState('')
  const [streamingSpeaker, setStreamingSpeaker] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, streamingContent])

  const startExperiment = async () => {
    setIsRunning(true)
    setMessages([])
    setCurrentTurn(0)
    setCurrentAgent(0)
    setConversationHistory([])
    setCurrentMessage("Hello! I'm looking forward to our conversation.")
    
    await runNextTurn(0, 0, [], "Hello! I'm looking forward to our conversation.")
  }

  const runNextTurn = async (turn: number, agent: number, history: { role: string; content: string }[], message: string) => {
    if (turn >= config.numTurns) {
      setIsRunning(false)
      return
    }

    try {
      const response = await fetch('/api/experiment/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          config,
          currentTurn: turn,
          currentAgent: agent,
          conversationHistory: history,
          currentMessage: message,
        }),
      })

      if (!response.body) {
        throw new Error('No response body')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let fullContent = ''

      setStreamingContent('')
      setStreamingSpeaker(config.agents[agent].name)

      while (true) {
        const { done, value } = await reader.read()
        
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        const lines = chunk.split('\n')
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              
              if (data.type === 'text') {
                setStreamingContent(prev => prev + data.content)
                fullContent += data.content
              } else if (data.type === 'complete') {
                const newMessage: Message = {
                  speaker: data.speaker,
                  content: data.fullContent,
                  turn: data.currentTurn,
                  agent: data.currentAgent,
                  timestamp: new Date()
                }
                
                setMessages(prev => [...prev, newMessage])
                setStreamingContent('')
                setStreamingSpeaker('')
                
                const newHistory = [
                  ...history,
                  { role: 'user', content: message },
                  { role: 'assistant', content: data.fullContent }
                ]
                
                if (!data.finished) {
                  setCurrentTurn(data.nextTurn)
                  setCurrentAgent(data.nextAgent)
                  setConversationHistory(newHistory)
                  setCurrentMessage(data.fullContent)
                  
                  setTimeout(() => {
                    runNextTurn(data.nextTurn, data.nextAgent, newHistory, data.fullContent)
                  }, 1000)
                } else {
                  setIsRunning(false)
                }
                break
              } else if (data.type === 'error') {
                console.error('Stream error:', data.error)
                setIsRunning(false)
                break
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e)
            }
          }
        }
      }
    } catch (error) {
      console.error('Error running experiment:', error)
      setIsRunning(false)
    }
  }

  const stopExperiment = () => {
    setIsRunning(false)
    setStreamingContent('')
    setStreamingSpeaker('')
  }

  const getAgentColor = (agentIndex: number) => {
    const colors = [
      'bg-orange-100 text-orange-800 border-orange-200',
      'bg-amber-100 text-amber-800 border-amber-200',
      'bg-yellow-100 text-yellow-800 border-yellow-200',
      'bg-lime-100 text-lime-800 border-lime-200',
      'bg-emerald-100 text-emerald-800 border-emerald-200'
    ]
    return colors[agentIndex % colors.length]
  }

  return (
    <div className="space-y-6">
      <Card className="backdrop-blur-sm bg-card/50 border-border/50">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-5 h-5 text-primary" />
                Experiment Status
              </CardTitle>
              <CardDescription>
                {config.agents.length} agents • {config.numTurns} turns • {config.modelName}
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={onReset}>
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Config
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap items-center gap-4">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm font-medium">
                Turn {currentTurn + 1} of {config.numTurns}
              </span>
            </div>
            
            <div className="flex items-center gap-2">
              <MessageCircle className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">
                {messages.length} messages
              </span>
            </div>

            <div className="flex-1" />
            
            {!isRunning ? (
              <Button 
                onClick={startExperiment}
                className="gap-2 bg-gradient-to-r from-primary to-primary/80"
              >
                <Play className="w-4 h-4" />
                Start Experiment
              </Button>
            ) : (
              <Button 
                onClick={stopExperiment}
                variant="destructive"
                className="gap-2"
              >
                <Square className="w-4 h-4" />
                Stop
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      <Card className="backdrop-blur-sm bg-card/50 border-border/50">
        <CardHeader>
          <CardTitle>Live Conversation</CardTitle>
          <CardDescription>
            Watch the agents converse in real-time
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4 max-h-96 overflow-y-auto">
            {messages.map((message, index) => (
              <div
                key={index}
                className={cn(
                  "p-4 rounded-lg border transition-all duration-200",
                  "bg-gradient-to-r from-card to-card/50"
                )}
              >
                <div className="flex items-center justify-between mb-2">
                  <Badge 
                    variant="outline" 
                    className={getAgentColor(message.agent)}
                  >
                    {message.speaker}
                  </Badge>
                  <span className="text-xs text-muted-foreground">
                    Turn {message.turn + 1}
                  </span>
                </div>
                <p className="text-sm leading-relaxed whitespace-pre-wrap">
                  {message.content}
                </p>
              </div>
            ))}
            
            {streamingContent && (
              <div className="p-4 rounded-lg border border-primary/20 bg-gradient-to-r from-primary/5 to-primary/10 animate-pulse">
                <div className="flex items-center justify-between mb-2">
                  <Badge 
                    variant="outline" 
                    className={getAgentColor(currentAgent)}
                  >
                    {streamingSpeaker}
                  </Badge>
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
                    <span className="text-xs text-muted-foreground">Typing...</span>
                  </div>
                </div>
                <p className="text-sm leading-relaxed whitespace-pre-wrap">
                  {streamingContent}
                  <span className="animate-pulse">|</span>
                </p>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </CardContent>
      </Card>

      {messages.length > 0 && !isRunning && (
        <Card className="backdrop-blur-sm bg-card/50 border-border/50">
          <CardHeader>
            <CardTitle>Experiment Complete</CardTitle>
            <CardDescription>
              What would you like to do with this conversation?
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4">
              <Button className="gap-2" disabled>
                <Save className="w-4 h-4" />
                Save Results
                <Badge variant="secondary" className="ml-2">Coming Soon</Badge>
              </Button>
              <Button 
                variant="outline" 
                onClick={() => {
                  setMessages([])
                  setCurrentTurn(0)
                  setCurrentAgent(0)
                  setConversationHistory([])
                }}
                className="gap-2"
              >
                <X className="w-4 h-4" />
                Discard
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}