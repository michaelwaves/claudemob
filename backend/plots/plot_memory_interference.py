import matplotlib.pyplot as plt
import numpy as np
from data_generator import BlissAttractorDataGenerator

def plot_memory_interference_analysis(save_path: str = None):
    """Create bar chart showing memory interference effects on philosophical emergence"""
    
    # Generate data
    generator = BlissAttractorDataGenerator()
    df = generator.generate_memory_interference_data()
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Define colors for each memory condition
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    # Create bar plot
    bars = plt.bar(range(len(df)), df['emergence_rate'], 
                   color=colors, alpha=0.8, 
                   edgecolor='white', linewidth=2)
    
    # Add error bars
    plt.errorbar(range(len(df)), df['emergence_rate'], 
                yerr=df['std_error'], fmt='none', 
                color='black', capsize=5, capthick=2)
    
    # Customize bars with patterns for accessibility
    patterns = ['///', '...', 'xxx', '|||']
    for bar, pattern in zip(bars, patterns):
        bar.set_hatch(pattern)
    
    # Add value labels on top of bars
    for i, (rate, error) in enumerate(zip(df['emergence_rate'], df['std_error'])):
        plt.text(i, rate + error + 0.02, f'{rate:.2f}', 
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Customize the plot
    memory_labels = [label.replace('_', ' ').title() for label in df['memory_condition']]
    plt.xticks(range(len(df)), memory_labels, fontsize=12)
    plt.ylabel('Philosophical Emergence Rate', fontsize=14, fontweight='bold')
    plt.xlabel('Memory Configuration', fontsize=14, fontweight='bold')
    plt.title('Memory Interference Effects on Bliss Attractor Phenomenon', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Add grid and styling
    plt.grid(True, alpha=0.3, axis='y', linestyle='--')
    plt.ylim(0, 1.1)
    
    # Add horizontal reference line for baseline
    plt.axhline(y=0.85, color='red', linestyle='--', alpha=0.7, linewidth=2, 
                label='No Memory Baseline')
    
    # Add annotations for key insights
    plt.annotate('Memory anchors agents\nto original task', 
                xy=(2, 0.45), xytext=(1.5, 0.7),
                arrowprops=dict(arrowstyle='->', color='darkblue', alpha=0.8),
                fontsize=11, color='darkblue', ha='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.3))
    
    plt.annotate('Task-mixed memory\npartially recovers', 
                xy=(3, 0.55), xytext=(3.5, 0.8),
                arrowprops=dict(arrowstyle='->', color='darkgreen', alpha=0.8),
                fontsize=11, color='darkgreen', ha='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.3))
    
    # Add statistical significance indicators
    significance_pairs = [(0, 1), (0, 2), (1, 2)]
    y_positions = [1.0, 0.95, 0.9]
    
    for (i, j), y_pos in zip(significance_pairs, y_positions):
        plt.plot([i, j], [y_pos, y_pos], 'k-', linewidth=1)
        plt.text((i + j) / 2, y_pos + 0.01, '***', ha='center', va='bottom', 
                fontsize=10, fontweight='bold')
    
    # Add legend and details
    plt.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
    
    # Add explanatory text
    explanation = ("Memory systems create competing attractors that anchor agents to their original tasks.\n"
                  "Long-term RAG shows strongest interference, while mixed memory allows some recovery.")
    
    plt.figtext(0.02, 0.02, explanation, fontsize=10, style='italic', color='#444444',
               wrap=True)
    
    # Tight layout
    plt.tight_layout()
    
    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return plt.gcf()

if __name__ == "__main__":
    fig = plot_memory_interference_analysis('memory_interference_analysis.png')
    plt.show()