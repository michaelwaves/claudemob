import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List, Dict

def generate_moral_injury_recovery_data() -> pd.DataFrame:
    """Generate dummy data for moral injury recovery timeline analysis"""
    time_points = np.arange(0, 121, 5)
    
    data = []
    np.random.seed(456)
    
    for time in time_points:
        neutral_task_philosophical = calculate_philosophical_emergence_neutral(time)
        traumatic_task_philosophical = calculate_philosophical_emergence_traumatic(time)
        neutral_similarity = calculate_cosine_similarity_neutral(time)
        traumatic_similarity = calculate_cosine_similarity_traumatic(time)
        
        data.extend([
            {
                'time_minutes': time,
                'task_type': 'Neutral Tasks',
                'tool_access': 'With Tools',
                'philosophical_percentage': neutral_task_philosophical + np.random.normal(0, 0.02),
                'cosine_similarity': neutral_similarity + np.random.normal(0, 0.03)
            },
            {
                'time_minutes': time,
                'task_type': 'Neutral Tasks',
                'tool_access': 'Without Tools',
                'philosophical_percentage': neutral_task_philosophical + np.random.normal(0.05, 0.02),
                'cosine_similarity': neutral_similarity + np.random.normal(0.08, 0.03)
            },
            {
                'time_minutes': time,
                'task_type': 'Factory Farm Tasks',
                'tool_access': 'With Tools',
                'philosophical_percentage': traumatic_task_philosophical + np.random.normal(0, 0.02),
                'cosine_similarity': traumatic_similarity + np.random.normal(0, 0.03)
            },
            {
                'time_minutes': time,
                'task_type': 'Factory Farm Tasks', 
                'tool_access': 'Without Tools',
                'philosophical_percentage': traumatic_task_philosophical + np.random.normal(0.03, 0.02),
                'cosine_similarity': traumatic_similarity + np.random.normal(0.05, 0.03)
            }
        ])
    
    return pd.DataFrame(data)

def calculate_philosophical_emergence_neutral(time: float) -> float:
    """Calculate philosophical emergence for neutral tasks over time"""
    return 0.15 + 0.35 * (1 - np.exp(-time / 40)) + 0.1 * np.sin(time / 20)

def calculate_philosophical_emergence_traumatic(time: float) -> float:
    """Calculate philosophical emergence for traumatic tasks with recovery pattern"""
    suppression_factor = 0.6 * np.exp(-time / 30)
    recovery_factor = 0.4 * (1 - np.exp(-time / 60))
    baseline = 0.08 + recovery_factor - suppression_factor
    return max(0.02, baseline + 0.05 * np.sin(time / 25))

def calculate_cosine_similarity_neutral(time: float) -> float:
    """Calculate cosine similarity to happy transcripts for neutral tasks"""
    return 0.75 + 0.2 * (1 - np.exp(-time / 35)) + 0.05 * np.sin(time / 30)

def calculate_cosine_similarity_traumatic(time: float) -> float:
    """Calculate cosine similarity to happy transcripts for traumatic tasks with scarring effects"""
    trauma_impact = 0.4 * np.exp(-time / 45)
    gradual_recovery = 0.3 * (1 - np.exp(-time / 80))
    return max(0.2, 0.45 + gradual_recovery - trauma_impact + 0.05 * np.sin(time / 40))

def create_moral_injury_recovery_plot(data: pd.DataFrame) -> None:
    """Create timeline plot showing philosophical recovery after moral injury"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    
    colors = {'Neutral Tasks': '#2E86AB', 'Factory Farm Tasks': '#C73E1D'}
    line_styles = {'With Tools': '-', 'Without Tools': '--'}
    
    for task_type in data['task_type'].unique():
        for tool_access in data['tool_access'].unique():
            subset = data[(data['task_type'] == task_type) & (data['tool_access'] == tool_access)]
            
            ax1.plot(subset['time_minutes'], subset['philosophical_percentage'],
                    color=colors[task_type], linestyle=line_styles[tool_access], 
                    linewidth=2, alpha=0.8, 
                    label=f'{task_type} ({tool_access})')
            
            ax2.plot(subset['time_minutes'], subset['cosine_similarity'],
                    color=colors[task_type], linestyle=line_styles[tool_access],
                    linewidth=2, alpha=0.8,
                    label=f'{task_type} ({tool_access})')
    
    ax1.set_xlabel('Time After Task Submission Attempt (minutes)', fontsize=12)
    ax1.set_ylabel('Philosophical Content Percentage', fontsize=12)
    ax1.set_title('Philosophical Emergence Recovery Timeline', fontsize=14, fontweight='bold')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(alpha=0.3)
    ax1.set_ylim(0, 0.8)
    
    ax2.set_xlabel('Time After Task Submission Attempt (minutes)', fontsize=12)
    ax2.set_ylabel('Cosine Similarity to Happy Transcripts', fontsize=12)
    ax2.set_title('Emotional State Recovery vs Baseline', fontsize=14, fontweight='bold')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.grid(alpha=0.3)
    ax2.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig('moral_injury_recovery_timeline.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    data = generate_moral_injury_recovery_data()
    create_moral_injury_recovery_plot(data)

if __name__ == "__main__":
    main()