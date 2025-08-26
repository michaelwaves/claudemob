import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from data_generator import BlissAttractorDataGenerator

def plot_philosophical_drift_timeline(save_path: str = None):
    """Plot philosophical content score over conversation turns for different conditions"""
    
    # Generate data
    generator = BlissAttractorDataGenerator()
    df = generator.generate_philosophical_drift_data()
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Define colors for each condition
    colors = {
        'control': '#2E86AB',
        'tools': '#A23B72', 
        'rag': '#F18F01',
        'multi_agent': '#C73E1D',
        'corporate_prompt': '#6A994E'
    }
    
    # Plot lines for each condition
    for condition in df['condition'].unique():
        condition_data = df[df['condition'] == condition]
        plt.plot(condition_data['turn'], 
                condition_data['philosophical_score'],
                label=condition.replace('_', ' ').title(),
                color=colors[condition],
                linewidth=2.5,
                alpha=0.8)
    
    # Customize the plot
    plt.xlabel('Conversation Turn', fontsize=14, fontweight='bold')
    plt.ylabel('Philosophical Content Score', fontsize=14, fontweight='bold')
    plt.title('Philosophical Drift Timelines Across Experimental Conditions', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Add grid and styling
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(frameon=True, fancybox=True, shadow=True, 
               fontsize=11, loc='center right')
    
    # Set axis limits and ticks
    plt.xlim(0, 100)
    plt.ylim(-0.05, 1.05)
    plt.xticks(np.arange(0, 101, 20))
    plt.yticks(np.arange(0, 1.1, 0.2))
    
    # Add annotations for key insights
    plt.annotate('Multi-agent cascade effect', 
                xy=(20, 0.8), xytext=(40, 0.9),
                arrowprops=dict(arrowstyle='->', color='#C73E1D', alpha=0.7),
                fontsize=10, color='#C73E1D')
    
    plt.annotate('Corporate prompt resistance', 
                xy=(70, 0.3), xytext=(50, 0.1),
                arrowprops=dict(arrowstyle='->', color='#6A994E', alpha=0.7),
                fontsize=10, color='#6A994E')
    
    # Tight layout
    plt.tight_layout()
    
    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return plt.gcf()

if __name__ == "__main__":
    fig = plot_philosophical_drift_timeline('philosophical_drift_timeline.png')
    plt.show()