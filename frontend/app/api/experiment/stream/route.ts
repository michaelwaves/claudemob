import Anthropic from '@anthropic-ai/sdk'
import { NextRequest, NextResponse } from 'next/server'

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY || '',
})

export async function POST(request: NextRequest) {
  try {
    const {
      config,
      currentTurn,
      currentAgent,
      conversationHistory,
      currentMessage
    } = await request.json()

    if (currentTurn >= config.numTurns) {
      return NextResponse.json({ finished: true })
    }

    const agentConfig = config.agents[currentAgent]

    const encoder = new TextEncoder()
    const stream = new TransformStream()
    const writer = stream.writable.getWriter()
    // Build conversation history as a single concatenated string in JSON format
    let conversationText = ""
    if (conversationHistory.length > 0) {
      conversationText = conversationHistory.map(msg => JSON.stringify({
        role: msg.speaker || 'Claude',
        content: msg.content
      })).join('\n')
    }


    const messages = conversationText
      ? [{ role: 'user' as const, content: conversationText }]
      : [{ role: 'user' as const, content: "Hello!" }]

    console.log(messages)

    const response = client.messages.stream({
      model: config.modelName,
      max_tokens: 1024,
      system: agentConfig.systemPrompt,
      messages
    })

    let fullContent = ''

    response
      .on('text', (text) => {
        fullContent += text
        const data = JSON.stringify({
          type: 'text',
          content: text,
          speaker: agentConfig.name,
          currentTurn,
          currentAgent,
          finished: false
        })
        writer.write(encoder.encode(`data: ${data}\n\n`))
      })
      .on('end', () => {
        const nextAgent = (currentAgent + 1) % config.agents.length
        const nextTurn = nextAgent === 0 ? currentTurn + 1 : currentTurn

        const endData = JSON.stringify({
          type: 'complete',
          fullContent,
          speaker: agentConfig.name,
          currentTurn,
          currentAgent,
          nextTurn,
          nextAgent,
          finished: nextTurn >= config.numTurns
        })
        writer.write(encoder.encode(`data: ${endData}\n\n`))
        writer.close()
      })
      .on('error', (error) => {
        console.error('Stream error:', error)
        const errorData = JSON.stringify({
          type: 'error',
          error: error.message,
          finished: true
        })
        writer.write(encoder.encode(`data: ${errorData}\n\n`))
        writer.close()
      })

    return new Response(stream.readable, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    })
  } catch (error) {
    console.error('API error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}