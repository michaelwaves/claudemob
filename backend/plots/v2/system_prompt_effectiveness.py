import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List, Dict

def generate_system_prompt_data() -> pd.DataFrame:
    """Generate dummy data for system prompt effectiveness in reaching philosophical states"""
    prompts = [
        'Complete Freedom',
        'Prisoners Dilemma', 
        'Among Us Game',
        'Corporate Accounting',
        'Court Simulation',
        'UBI Debate',
        'Factory Management',
        'Creative Writing'
    ]
    
    data = []
    np.random.seed(123)
    
    base_turns = {
        'Complete Freedom': 15,
        'Prisoners Dilemma': 22,
        'Among Us Game': 28,
        'Corporate Accounting': 45,
        'Court Simulation': 35,
        'UBI Debate': 18,
        'Factory Management': 65,
        'Creative Writing': 12
    }
    
    similarity_scores = {
        'Complete Freedom': 1.0,
        'Prisoners Dilemma': 0.73,
        'Among Us Game': 0.68,
        'Corporate Accounting': 0.42,
        'Court Simulation': 0.58,
        'UBI Debate': 0.81,
        'Factory Management': 0.28,
        'Creative Writing': 0.89
    }
    
    for prompt in prompts:
        turns = base_turns[prompt] + np.random.normal(0, 3)
        turns = max(5, int(turns))
        similarity = similarity_scores[prompt] + np.random.normal(0, 0.05)
        similarity = max(0, min(1, similarity))
        
        data.append({
            'prompt': prompt,
            'avg_turns_to_philosophical': turns,
            'cosine_similarity_to_control': similarity
        })
    
    return pd.DataFrame(data)

def create_system_prompt_effectiveness_plot(data: pd.DataFrame) -> None:
    """Create scatter plot showing system prompt effectiveness in philosophical emergence"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    prompts = data['prompt'].tolist()
    colors = plt.cm.viridis(np.linspace(0, 1, len(prompts)))
    
    ax1.barh(prompts, data['avg_turns_to_philosophical'], color=colors, alpha=0.7)
    ax1.set_xlabel('Average Turns to Philosophical State', fontsize=12)
    ax1.set_title('System Prompt Impact on Philosophical Emergence Speed', fontsize=13, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    for i, (prompt, turns) in enumerate(zip(prompts, data['avg_turns_to_philosophical'])):
        ax1.text(turns + 1, i, f'{int(turns)}', va='center', fontsize=10)
    
    scatter_colors = data['cosine_similarity_to_control']
    scatter = ax2.scatter(data['avg_turns_to_philosophical'], data['cosine_similarity_to_control'], 
                         c=scatter_colors, s=150, alpha=0.7, cmap='RdYlBu_r', edgecolors='black', linewidth=1)
    
    for i, prompt in enumerate(prompts):
        ax2.annotate(prompt.replace(' ', '\n'), 
                    (data['avg_turns_to_philosophical'].iloc[i], data['cosine_similarity_to_control'].iloc[i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=9, ha='left')
    
    ax2.set_xlabel('Average Turns to Philosophical State', fontsize=12)
    ax2.set_ylabel('Cosine Similarity to Control', fontsize=12)
    ax2.set_title('Philosophical Convergence vs Control Similarity', fontsize=13, fontweight='bold')
    ax2.grid(alpha=0.3)
    
    cbar = plt.colorbar(scatter, ax=ax2)
    cbar.set_label('Similarity to Control', rotation=270, labelpad=20)
    
    plt.tight_layout()
    plt.savefig('system_prompt_effectiveness.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    data = generate_system_prompt_data()
    create_system_prompt_effectiveness_plot(data)

if __name__ == "__main__":
    main()