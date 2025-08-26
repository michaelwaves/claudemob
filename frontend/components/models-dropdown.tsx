'use client'

import { useState } from 'react'
import { Check, ChevronDown } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface ModelsDropdownProps {
    value: string
    onChange: (value: string) => void
    className?: string
}

function ModelsDropdown({ value, onChange, className = '' }: ModelsDropdownProps) {
    const [isOpen, setIsOpen] = useState(false)

    const models = [
        "claude-opus-4-1-20250805",
        "claude-opus-4-20250514",
        "claude-sonnet-4-20250514",
        "claude-3-7-sonnet-latest",
        "claude-3-5-haiku-latest",
        "claude-3-haiku-20240307"
    ]

    const handleSelect = (model: string) => {
        onChange(model)
        setIsOpen(false)
    }

    return (
        <div className={`relative ${className}`}>
            <Button
                type="button"
                variant="outline"
                className="w-full justify-between bg-background/50 text-left font-normal"
                onClick={() => setIsOpen(!isOpen)}
            >
                <span className="truncate">{value || "Select a model..."}</span>
                <ChevronDown className={`h-4 w-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
            </Button>

            {isOpen && (
                <div className="absolute top-full left-0 right-0 z-50 mt-1 rounded-md border bg-popover shadow-lg">
                    <div className="max-h-60 overflow-auto p-1">
                        {models.map((model) => (
                            <button
                                key={model}
                                type="button"
                                className="flex w-full items-center justify-between rounded-sm px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground outline-none"
                                onClick={() => handleSelect(model)}
                            >
                                <span className="truncate">{model}</span>
                                {value === model && <Check className="h-4 w-4" />}
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}

export default ModelsDropdown;