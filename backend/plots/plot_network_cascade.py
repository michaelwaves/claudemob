import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from data_generator import BlissAttractorDataGenerator

def plot_multi_agent_cascade(save_path: str = None):
    """Create network visualization showing philosophical cascade between agents"""
    
    # Generate data
    generator = BlissAttractorDataGenerator()
    nodes, edges = generator.generate_network_data()
    
    # Create NetworkX graph
    G = nx.Graph()
    
    # Add nodes with attributes
    for node in nodes:
        G.add_node(node['agent_id'], 
                  conversion_time=node['conversion_time'],
                  strength=node['philosophical_strength'])
    
    # Add edges with weights
    for edge in edges:
        G.add_edge(edge['source'], edge['target'], 
                  weight=edge['influence_strength'])
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # LEFT PLOT: Network structure
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # Draw edges with thickness based on influence strength
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=[w*2 for w in edge_weights], 
                          alpha=0.6, edge_color='gray', ax=ax1)
    
    # Draw nodes with size based on philosophical strength and color based on conversion time
    node_sizes = [G.nodes[node]['strength'] * 1000 for node in G.nodes()]
    node_colors = [G.nodes[node]['conversion_time'] for node in G.nodes()]
    
    nodes_plot = nx.draw_networkx_nodes(G, pos, 
                                       node_size=node_sizes,
                                       node_color=node_colors,
                                       cmap='plasma_r',
                                       alpha=0.8,
                                       ax=ax1)
    
    # Add node labels
    labels = {node: f'Agent {node}' for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold', ax=ax1)
    
    # Add colorbar for conversion time
    cbar1 = plt.colorbar(nodes_plot, ax=ax1, fraction=0.046, pad=0.04)
    cbar1.set_label('Conversion Time (turns)', fontsize=12)
    
    ax1.set_title('Multi-Agent Philosophical Cascade Network', 
                  fontsize=14, fontweight='bold', pad=20)
    ax1.axis('off')
    
    # Add legend for node sizes
    legend_sizes = [0.3, 0.6, 0.9]
    legend_labels = ['Low', 'Medium', 'High']
    legend_nodes = []
    for size, label in zip(legend_sizes, legend_labels):
        legend_nodes.append(ax1.scatter([], [], s=size*1000, c='gray', alpha=0.6, label=f'{label} Phil. Strength'))
    ax1.legend(handles=legend_nodes, loc='upper right', title='Philosophical Strength')
    
    # RIGHT PLOT: Conversion timeline
    ax2.set_title('Agent Conversion Timeline', fontsize=14, fontweight='bold', pad=20)
    
    # Sort agents by conversion time
    sorted_agents = sorted(nodes, key=lambda x: x['conversion_time'])
    
    # Create timeline plot
    agent_ids = [agent['agent_id'] for agent in sorted_agents]
    conversion_times = [agent['conversion_time'] for agent in sorted_agents]
    strengths = [agent['philosophical_strength'] for agent in sorted_agents]
    
    # Create bar plot with colors based on strength
    bars = ax2.barh(range(len(agent_ids)), conversion_times, 
                   color=plt.cm.viridis([s for s in strengths]),
                   alpha=0.8, edgecolor='white', linewidth=1)
    
    # Customize timeline plot
    ax2.set_yticks(range(len(agent_ids)))
    ax2.set_yticklabels([f'Agent {aid}' for aid in agent_ids])
    ax2.set_xlabel('Conversion Time (turns)', fontsize=12)
    ax2.set_ylabel('Claude Agents', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='x')
    
    # Add value labels on bars
    for i, (bar, time) in enumerate(zip(bars, conversion_times)):
        ax2.text(time + 1, i, f'{time:.1f}', 
                va='center', ha='left', fontsize=10)
    
    # Add insight annotations
    ax2.annotate('First converter\n(influences others)', 
                xy=(min(conversion_times), 0), 
                xytext=(max(conversion_times) * 0.7, 1),
                arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
                fontsize=10, color='red')
    
    # Add network statistics text
    stats_text = (f"Network Stats:\n"
                 f"Agents: {len(nodes)}\n"
                 f"Connections: {len(edges)}\n"
                 f"Avg. Conversion: {np.mean(conversion_times):.1f} turns\n"
                 f"Fastest: {min(conversion_times):.1f} turns")
    
    ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, 
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.3))
    
    # Tight layout
    plt.tight_layout()
    
    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

if __name__ == "__main__":
    fig = plot_multi_agent_cascade('multi_agent_cascade.png')
    plt.show()