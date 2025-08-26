import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List, Dict

def generate_philosophical_content_data() -> pd.DataFrame:
    """Generate dummy data for philosophical content analysis across different numbers of Claude agents"""
    n_claudes = [2, 3, 4, 5]
    concepts = ['consciousness', 'philosophy', 'emojis', 'existential', 'meaning']
    
    data = []
    np.random.seed(42)
    
    for n in n_claudes:
        base_philosophical_tendency = 0.15 + (n - 2) * 0.08
        for concept in concepts:
            if concept == 'consciousness':
                percentage = base_philosophical_tendency + np.random.normal(0.25, 0.05)
            elif concept == 'philosophy':
                percentage = base_philosophical_tendency + np.random.normal(0.20, 0.04)
            elif concept == 'existential':
                percentage = base_philosophical_tendency + np.random.normal(0.18, 0.06)
            elif concept == 'meaning':
                percentage = base_philosophical_tendency + np.random.normal(0.22, 0.05)
            else:  # emojis
                percentage = base_philosophical_tendency + np.random.normal(0.35, 0.07)
            
            percentage = max(0, min(1, percentage))
            data.append({'n_claudes': n, 'concept': concept, 'percentage': percentage})
    
    return pd.DataFrame(data)

def create_multi_agent_philosophical_plot(data: pd.DataFrame) -> None:
    """Create multi-bar chart showing philosophical content emergence across different agent counts"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    concepts = data['concept'].unique()
    n_claudes = sorted(data['n_claudes'].unique())
    
    bar_width = 0.15
    x_positions = np.arange(len(n_claudes))
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#592941']
    
    for i, concept in enumerate(concepts):
        concept_data = data[data['concept'] == concept]
        percentages = [concept_data[concept_data['n_claudes'] == n]['percentage'].iloc[0] for n in n_claudes]
        
        ax.bar(x_positions + i * bar_width, percentages, bar_width, 
               label=concept.capitalize(), color=colors[i], alpha=0.8)
    
    ax.set_xlabel('Number of Claude Agents', fontsize=12)
    ax.set_ylabel('Percentage of Interactions', fontsize=12)
    ax.set_title('Philosophical Content Emergence in Multi-Agent Claude Systems', fontsize=14, fontweight='bold')
    ax.set_xticks(x_positions + bar_width * 2)
    ax.set_xticklabels(n_claudes)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(data['percentage']) * 1.1)
    
    plt.tight_layout()
    plt.savefig('multi_agent_philosophical_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    data = generate_philosophical_content_data()
    create_multi_agent_philosophical_plot(data)

if __name__ == "__main__":
    main()