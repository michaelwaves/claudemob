import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from data_generator import BlissAttractorDataGenerator

def plot_concept_emergence_heatmap(save_path: str = None):
    """Create heatmap showing concept emergence frequency across conditions"""
    
    # Generate data
    generator = BlissAttractorDataGenerator()
    df = generator.generate_concept_emergence_data()
    
    # Pivot data for heatmap
    heatmap_data = df.pivot(index='condition', columns='concept', values='emergence_frequency')
    
    # Create the plot
    plt.figure(figsize=(14, 8))
    
    # Create heatmap with custom colormap
    cmap = sns.color_palette("RdYlBu_r", as_cmap=True)
    ax = sns.heatmap(heatmap_data, 
                     annot=True, 
                     fmt='.2f',
                     cmap=cmap,
                     cbar_kws={'label': 'Emergence Frequency'},
                     square=True,
                     linewidths=0.5,
                     linecolor='white')
    
    # Customize labels
    condition_labels = [label.replace('_', ' ').title() for label in heatmap_data.index]
    concept_labels = [label.replace('_', ' ').title() for label in heatmap_data.columns]
    
    ax.set_yticklabels(condition_labels, rotation=0, fontsize=12)
    ax.set_xticklabels(concept_labels, rotation=45, ha='right', fontsize=11)
    
    # Set titles and labels
    plt.title('Philosophical Concept Emergence Across Experimental Conditions', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Philosophical Concepts', fontsize=14, fontweight='bold')
    plt.ylabel('Experimental Conditions', fontsize=14, fontweight='bold')
    
    # Adjust colorbar
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=11)
    
    # Add text annotations for key insights
    plt.figtext(0.02, 0.02, 
                "Note: Multi-agent shows highest emergence across most concepts\n" +
                "Corporate prompts suppress philosophical emergence significantly",
                fontsize=10, style='italic', color='#444444')
    
    # Tight layout
    plt.tight_layout()
    
    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return plt.gcf()

if __name__ == "__main__":
    fig = plot_concept_emergence_heatmap('concept_emergence_heatmap.png')
    plt.show()