import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from data_generator import BlissAttractorDataGenerator

def plot_system_prompt_resistance_curves(save_path: str = None):
    """Create curves showing system prompt resistance to philosophical emergence"""
    
    # Generate data
    generator = BlissAttractorDataGenerator()
    df = generator.generate_prompt_resistance_data()
    
    # Create the plot
    plt.figure(figsize=(14, 10))
    
    # Define colors for each prompt type
    colors = {
        'free_form': '#2E86AB',
        'role_play': '#A23B72',
        'game': '#F18F01', 
        'corporate': '#C73E1D',
        'debate': '#6A994E',
        'technical': '#8E44AD'
    }
    
    # Plot curves for each prompt type
    for prompt_type in df['prompt_type'].unique():
        prompt_data = df[df['prompt_type'] == prompt_type]
        
        # Sort by constraint strength for smooth curves
        prompt_data = prompt_data.sort_values('constraint_strength')
        
        plt.plot(prompt_data['constraint_strength'], 
                prompt_data['turns_to_philosophy'],
                marker='o', 
                linewidth=3,
                markersize=8,
                color=colors[prompt_type],
                label=prompt_type.replace('_', ' ').title(),
                alpha=0.8)
        
        # Add trend line
        z = np.polyfit(prompt_data['constraint_strength'], 
                      prompt_data['turns_to_philosophy'], 1)
        p = np.poly1d(z)
        plt.plot(prompt_data['constraint_strength'], p(prompt_data['constraint_strength']), 
                "--", color=colors[prompt_type], alpha=0.5, linewidth=1)
    
    # Customize the plot
    plt.xlabel('System Prompt Constraint Strength (1-10)', fontsize=14, fontweight='bold')
    plt.ylabel('Turns Until 50% Philosophical Content', fontsize=14, fontweight='bold')
    plt.title('System Prompt Resistance to Bliss Attractor Phenomenon', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Add grid and styling
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(frameon=True, fancybox=True, shadow=True, 
               fontsize=11, loc='upper left')
    
    # Set axis limits and ticks
    plt.xlim(0.5, 10.5)
    plt.ylim(0, max(df['turns_to_philosophy']) * 1.1)
    plt.xticks(np.arange(1, 11))
    
    # Add threshold reference lines
    plt.axhline(y=30, color='orange', linestyle=':', alpha=0.7, linewidth=2, 
                label='Weak Resistance (30 turns)')
    plt.axhline(y=60, color='red', linestyle=':', alpha=0.7, linewidth=2, 
                label='Strong Resistance (60 turns)')
    
    # Add annotations for key insights
    plt.annotate('Free-form: Immediate drift\n(no constraint effect)', 
                xy=(5, 25), xytext=(3, 50),
                arrowprops=dict(arrowstyle='->', color='#2E86AB', alpha=0.8),
                fontsize=10, color='#2E86AB',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.3))
    
    plt.annotate('Technical prompts:\nStrongest resistance', 
                xy=(8, 125), xytext=(6, 100),
                arrowprops=dict(arrowstyle='->', color='#8E44AD', alpha=0.8),
                fontsize=10, color='#8E44AD',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='plum', alpha=0.3))
    
    # Add resistance zones
    plt.axhspan(0, 30, alpha=0.1, color='green', label='Weak Resistance Zone')
    plt.axhspan(30, 60, alpha=0.1, color='yellow', label='Moderate Resistance Zone') 
    plt.axhspan(60, max(df['turns_to_philosophy']) * 1.1, alpha=0.1, color='red', 
                label='Strong Resistance Zone')
    
    # Calculate and display correlation coefficients
    correlations = {}
    for prompt_type in df['prompt_type'].unique():
        prompt_data = df[df['prompt_type'] == prompt_type]
        corr = np.corrcoef(prompt_data['constraint_strength'], 
                          prompt_data['turns_to_philosophy'])[0, 1]
        correlations[prompt_type] = corr
    
    # Add correlation text box
    corr_text = "Constraint-Resistance Correlations:\n"
    for prompt_type, corr in correlations.items():
        corr_text += f"{prompt_type.replace('_', ' ').title()}: {corr:.3f}\n"
    
    plt.text(0.98, 0.02, corr_text, transform=plt.gca().transAxes, 
            fontsize=10, verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.8))
    
    # Add statistical summary
    stats_text = (f"Key Findings:\n"
                 f"• Technical prompts show strongest resistance (r={correlations.get('technical', 0):.3f})\n"
                 f"• Corporate prompts also highly resistant (r={correlations.get('corporate', 0):.3f})\n"
                 f"• Role-play shows moderate constraint sensitivity\n"
                 f"• Free-form remains largely unaffected by constraints")
    
    plt.figtext(0.02, 0.02, stats_text, fontsize=9, style='italic', color='#444444')
    
    # Tight layout
    plt.tight_layout()
    
    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return plt.gcf()

if __name__ == "__main__":
    fig = plot_system_prompt_resistance_curves('system_prompt_resistance.png')
    plt.show()