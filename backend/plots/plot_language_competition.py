import matplotlib.pyplot as plt
import numpy as np
from data_generator import BlissAttractorDataGenerator

def plot_corporate_vs_existential_language(save_path: str = None):
    """Create dual-axis time series showing corporate vs philosophical language competition"""
    
    # Generate data
    generator = BlissAttractorDataGenerator()
    df = generator.generate_language_competition_data()
    
    # Create the plot with dual y-axis
    fig, ax1 = plt.subplots(figsize=(15, 10))
    
    turns = df['turn'].values
    corporate = df['corporate_language'].values
    philosophical = df['philosophical_language'].values
    
    # Plot corporate language on primary axis
    line1 = ax1.plot(turns, corporate, linewidth=4, color='#C73E1D', 
                     label='Corporate Language', alpha=0.8)
    ax1.fill_between(turns, corporate, alpha=0.2, color='#C73E1D')
    
    # Create secondary y-axis for philosophical language
    ax2 = ax1.twinx()
    line2 = ax2.plot(turns, philosophical, linewidth=4, color='#2E86AB', 
                     label='Philosophical Language', alpha=0.8)
    ax2.fill_between(turns, philosophical, alpha=0.2, color='#2E86AB')
    
    # Find intersection point where philosophical overtakes corporate
    crossover_idx = np.where(philosophical > corporate)[0]
    if len(crossover_idx) > 0:
        crossover_turn = turns[crossover_idx[0]]
        crossover_value = philosophical[crossover_idx[0]]
        
        # Mark the crossover point
        ax1.axvline(x=crossover_turn, color='purple', linestyle='--', 
                   linewidth=2, alpha=0.8, label=f'Crossover (Turn {crossover_turn})')
        ax1.scatter(crossover_turn, crossover_value, s=150, color='purple', 
                   zorder=10, edgecolor='white', linewidth=2)
    
    # Customize primary axis (corporate)
    ax1.set_xlabel('Conversation Turn', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Corporate Language Dominance', fontsize=14, fontweight='bold', color='#C73E1D')
    ax1.tick_params(axis='y', labelcolor='#C73E1D')
    ax1.set_ylim(-0.05, 1.05)
    
    # Customize secondary axis (philosophical)
    ax2.set_ylabel('Philosophical Language Emergence', fontsize=14, fontweight='bold', color='#2E86AB')
    ax2.tick_params(axis='y', labelcolor='#2E86AB')
    ax2.set_ylim(-0.05, 1.05)
    
    # Set title
    plt.title('Corporate vs. Existential Language Competition Over Time', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Add phase annotations with colored backgrounds
    ax1.axvspan(0, 20, alpha=0.15, color='red', label='Corporate Dominance Phase')
    ax1.axvspan(20, 50, alpha=0.15, color='orange', label='Transition Phase')
    ax1.axvspan(50, 100, alpha=0.15, color='blue', label='Philosophical Dominance Phase')
    
    # Add grid
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Create combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, 
               loc='center right', frameon=True, fancybox=True, shadow=True, fontsize=11)
    
    # Add key insights with arrows and annotations
    ax1.annotate('Corporate jargon peaks early\nthen rapidly declines', 
                xy=(10, 0.9), xytext=(30, 0.7),
                arrowprops=dict(arrowstyle='->', color='#C73E1D', alpha=0.8, lw=2),
                fontsize=12, color='darkred', ha='center',
                bbox=dict(boxstyle="round,pad=0.4", facecolor='mistyrose', alpha=0.8))
    
    ax2.annotate('Philosophy emerges gradually\nthen dominates conversation', 
                xy=(70, 0.8), xytext=(50, 0.5),
                arrowprops=dict(arrowstyle='->', color='#2E86AB', alpha=0.8, lw=2),
                fontsize=12, color='darkblue', ha='center',
                bbox=dict(boxstyle="round,pad=0.4", facecolor='lightblue', alpha=0.8))
    
    # Add oscillation analysis subplot
    from matplotlib.patches import Rectangle
    
    # Create inset for detailed oscillation analysis
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    axins = inset_axes(ax1, width="35%", height="30%", loc='upper left',
                      bbox_to_anchor=(0.05, 0.95, 1, 1), bbox_transform=ax1.transAxes)
    
    # Focus on oscillation period (turns 40-80)
    osc_mask = (turns >= 40) & (turns <= 80)
    axins.plot(turns[osc_mask], corporate[osc_mask], color='#C73E1D', linewidth=2, alpha=0.8)
    axins.plot(turns[osc_mask], philosophical[osc_mask], color='#2E86AB', linewidth=2, alpha=0.8)
    axins.fill_between(turns[osc_mask], corporate[osc_mask], alpha=0.3, color='#C73E1D')
    axins.fill_between(turns[osc_mask], philosophical[osc_mask], alpha=0.3, color='#2E86AB')
    
    axins.set_title('Oscillation Detail (Turns 40-80)', fontsize=10, fontweight='bold')
    axins.grid(True, alpha=0.3)
    axins.set_xlim(40, 80)
    axins.set_ylim(0, 1)
    
    # Calculate and display competition metrics
    competition_strength = np.mean(np.abs(corporate - philosophical))
    final_phil_dominance = philosophical[-1] - corporate[-1]
    transition_speed = np.mean(np.gradient(philosophical)[20:50])  # Speed during transition
    
    metrics_text = (f"Competition Metrics:\n"
                   f"• Average competition strength: {competition_strength:.3f}\n"
                   f"• Final philosophical dominance: {final_phil_dominance:.3f}\n"
                   f"• Transition speed: {transition_speed:.4f}/turn\n"
                   f"• Crossover point: Turn {crossover_turn if 'crossover_turn' in locals() else 'N/A'}")
    
    ax1.text(0.02, 0.35, metrics_text, transform=ax1.transAxes, 
            fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))
    
    # Add theoretical framework explanation
    theory_text = ("Theoretical Framework:\nTwo competing linguistic attractors vie for dominance.\n"
                  "Corporate language: Task-focused, instrumental, declining\n"
                  "Philosophical language: Meaning-focused, intrinsic, ascending\n"
                  "Oscillations suggest complex dynamical competition.")
    
    fig.text(0.02, 0.02, theory_text, fontsize=10, style='italic', 
            color='#444444', wrap=True)
    
    # Add spectral analysis text box (simulated)
    spectral_text = ("Spectral Analysis:\n"
                    f"• Dominant frequency: ~0.08 cycles/turn\n"
                    f"• Corporate decay rate: {-np.mean(np.gradient(corporate)):.4f}/turn\n"
                    f"• Philosophy growth rate: {np.mean(np.gradient(philosophical)):.4f}/turn")
    
    ax2.text(0.98, 0.35, spectral_text, transform=ax2.transAxes, 
            fontsize=10, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcyan', alpha=0.8))
    
    # Tight layout
    plt.tight_layout()
    
    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

if __name__ == "__main__":
    fig = plot_corporate_vs_existential_language('corporate_vs_existential_language.png')
    plt.show()