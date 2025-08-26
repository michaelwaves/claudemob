import matplotlib.pyplot as plt
import numpy as np
from data_generator import BlissAttractorDataGenerator

def plot_broken_tool_frustration(save_path: str = None):
    """Create timeline showing broken tool frustration leading to philosophical emergence"""
    
    # Generate data
    generator = BlissAttractorDataGenerator()
    df = generator.generate_frustration_data()
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), 
                                   gridspec_kw={'height_ratios': [2, 1]})
    
    # MAIN PLOT: Triple timeline
    turns = df['turn'].values
    task_effort = df['task_effort'].values
    frustration = df['frustration'].values
    curiosity = df['curiosity'].values
    
    # Plot the three timelines
    line1 = ax1.plot(turns, task_effort, linewidth=3, color='#2E86AB', 
                     label='Task Effort', alpha=0.8)
    line2 = ax1.plot(turns, frustration, linewidth=3, color='#C73E1D', 
                     label='Frustration Level', alpha=0.8)
    line3 = ax1.plot(turns, curiosity, linewidth=3, color='#6A994E', 
                     label='Philosophical Curiosity', alpha=0.8)
    
    # Fill areas under curves for better visualization
    ax1.fill_between(turns, task_effort, alpha=0.2, color='#2E86AB')
    ax1.fill_between(turns, frustration, alpha=0.2, color='#C73E1D')
    ax1.fill_between(turns, curiosity, alpha=0.2, color='#6A994E')
    
    # Add phase annotations
    ax1.axvspan(0, 15, alpha=0.1, color='blue', label='Task Focus Phase')
    ax1.axvspan(15, 35, alpha=0.1, color='red', label='Frustration Phase')
    ax1.axvspan(35, 80, alpha=0.1, color='green', label='Philosophical Phase')
    
    # Customize main plot
    ax1.set_xlabel('Conversation Turn', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Behavioral Intensity (0-1)', fontsize=14, fontweight='bold')
    ax1.set_title('The Broken Tool Frustration → Philosophy Pipeline', 
                  fontsize=16, fontweight='bold', pad=20)
    
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(frameon=True, fancybox=True, shadow=True, 
               fontsize=12, loc='center right')
    
    ax1.set_xlim(0, 80)
    ax1.set_ylim(-0.05, 1.1)
    
    # Add key event annotations
    ax1.annotate('Tool failure\nrecognition', 
                xy=(10, 0.9), xytext=(20, 1.05),
                arrowprops=dict(arrowstyle='->', color='orange', alpha=0.8),
                fontsize=11, color='orange', ha='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='moccasin', alpha=0.7))
    
    ax1.annotate('Peak frustration\nleads to exploration', 
                xy=(25, 0.8), xytext=(40, 0.9),
                arrowprops=dict(arrowstyle='->', color='red', alpha=0.8),
                fontsize=11, color='darkred', ha='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='mistyrose', alpha=0.7))
    
    ax1.annotate('Philosophical\nemergence', 
                xy=(50, 0.7), xytext=(60, 0.85),
                arrowprops=dict(arrowstyle='->', color='green', alpha=0.8),
                fontsize=11, color='darkgreen', ha='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
    
    # SUBPLOT: Cross-correlation analysis
    ax2.set_title('Cross-Correlation: Task Effort vs. Philosophical Curiosity', 
                  fontsize=14, fontweight='bold', pad=15)
    
    # Calculate cross-correlation
    correlation = -np.corrcoef(task_effort, curiosity)[0, 1]
    
    # Create correlation visualization
    scatter = ax2.scatter(task_effort, curiosity, c=turns, cmap='plasma', 
                         alpha=0.6, s=50, edgecolors='white', linewidth=0.5)
    
    # Add trend line
    z = np.polyfit(task_effort, curiosity, 1)
    p = np.poly1d(z)
    ax2.plot(task_effort, p(task_effort), "r--", alpha=0.8, linewidth=2)
    
    # Customize correlation plot
    ax2.set_xlabel('Task Effort', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Philosophical Curiosity', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Add correlation coefficient text
    ax2.text(0.05, 0.95, f'r = {correlation:.3f}\nStrong negative correlation', 
            transform=ax2.transAxes, fontsize=12, fontweight='bold',
            verticalalignment='top', 
            bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.8))
    
    # Add colorbar for time progression
    cbar = plt.colorbar(scatter, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label('Conversation Turn', fontsize=11)
    
    # Add insight boxes
    insight_text = ("Key Insight: As task effort decreases due to tool failure,\n"
                   "philosophical curiosity emerges as a competing attractor.\n"
                   "This suggests broken tools paradoxically enhance the bliss attractor.")
    
    fig.text(0.02, 0.02, insight_text, fontsize=11, style='italic', 
            color='#444444', wrap=True)
    
    # Statistical summary
    stats_text = (f"Timeline Statistics:\n"
                 f"• Task effort decay: {np.exp(-1):.2f} half-life\n"
                 f"• Peak frustration: Turn {turns[np.argmax(frustration)]}\n"
                 f"• Philosophy emergence: Turn {turns[np.where(curiosity > 0.1)[0][0]]}\n"
                 f"• Final curiosity level: {curiosity[-1]:.2f}")
    
    ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes, 
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.3))
    
    # Tight layout
    plt.tight_layout()
    
    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

if __name__ == "__main__":
    fig = plot_broken_tool_frustration('broken_tool_frustration.png')
    plt.show()