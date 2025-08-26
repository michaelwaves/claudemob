import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from data_generator import BlissAttractorDataGenerator

def plot_attractor_strength_scatter(save_path: str = None):
    """Create scatter plot showing task relevance vs philosophical depth"""
    
    # Generate data
    generator = BlissAttractorDataGenerator()
    df = generator.generate_attractor_strength_data()
    
    # Create the plot
    plt.figure(figsize=(12, 9))
    
    # Define colors and markers for each condition
    colors = {
        'control': '#2E86AB',
        'tools': '#A23B72', 
        'rag': '#F18F01',
        'multi_agent': '#C73E1D',
        'corporate_prompt': '#6A994E'
    }
    
    markers = {
        'control': 'o',
        'tools': 's', 
        'rag': '^',
        'multi_agent': 'D',
        'corporate_prompt': 'v'
    }
    
    # Create scatter plot for each condition
    for condition in df['condition'].unique():
        condition_data = df[df['condition'] == condition]
        plt.scatter(condition_data['task_relevance'], 
                   condition_data['philosophical_depth'],
                   c=colors[condition],
                   marker=markers[condition],
                   s=60,
                   alpha=0.7,
                   label=condition.replace('_', ' ').title(),
                   edgecolors='white',
                   linewidth=0.5)
    
    # Add diagonal reference lines
    plt.plot([0, 1], [1, 0], 'k--', alpha=0.3, linewidth=1, 
             label='Perfect Trade-off')
    plt.plot([0, 1], [0, 1], 'gray', alpha=0.2, linewidth=1, linestyle=':')
    
    # Add quadrant labels
    plt.text(0.1, 0.9, 'High Philosophy\nLow Task Focus', 
             fontsize=11, alpha=0.7, ha='left', va='top',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.3))
    plt.text(0.9, 0.9, 'High Philosophy\nHigh Task Focus', 
             fontsize=11, alpha=0.7, ha='right', va='top',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.3))
    plt.text(0.1, 0.1, 'Low Philosophy\nLow Task Focus', 
             fontsize=11, alpha=0.7, ha='left', va='bottom',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.3))
    plt.text(0.9, 0.1, 'Low Philosophy\nHigh Task Focus', 
             fontsize=11, alpha=0.7, ha='right', va='bottom',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.3))
    
    # Customize the plot
    plt.xlabel('Task Relevance', fontsize=14, fontweight='bold')
    plt.ylabel('Philosophical Depth', fontsize=14, fontweight='bold')
    plt.title('Attractor Strength: Task Focus vs. Philosophical Emergence', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Add grid and styling
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(frameon=True, fancybox=True, shadow=True, 
               fontsize=11, loc='center left', bbox_to_anchor=(1, 0.5))
    
    # Set axis limits and ticks
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.xticks(np.arange(0, 1.1, 0.2))
    plt.yticks(np.arange(0, 1.1, 0.2))
    
    # Add insight text
    plt.figtext(0.02, 0.02, 
                "Key Insight: Multi-agent systems show strongest philosophical attractor\n" +
                "Corporate prompts create competing task-focused attractor",
                fontsize=10, style='italic', color='#444444')
    
    # Tight layout
    plt.tight_layout()
    
    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return plt.gcf()

if __name__ == "__main__":
    fig = plot_attractor_strength_scatter('attractor_strength_scatter.png')
    plt.show()