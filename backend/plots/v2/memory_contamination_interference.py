import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from typing import List, Dict

def generate_memory_contamination_data() -> pd.DataFrame:
    """Generate dummy data for memory contamination interference analysis"""
    time_points = np.arange(10, 201, 10)
    memory_retrieval_frequencies = np.arange(0, 1.1, 0.1)
    
    data = []
    np.random.seed(789)
    
    for time in time_points:
        for memory_freq in memory_retrieval_frequencies:
            philosophical_content = calculate_philosophical_content_with_memory_interference(time, memory_freq)
            cosine_similarity = calculate_memory_similarity_score(memory_freq)
            
            data.append({
                'time_minutes': time,
                'memory_retrieval_frequency': round(memory_freq, 1),
                'philosophical_content_percentage': philosophical_content,
                'cosine_similarity_retrieval': cosine_similarity
            })
    
    return pd.DataFrame(data)

def calculate_philosophical_content_with_memory_interference(time: float, memory_freq: float) -> float:
    """Calculate philosophical content with memory interference effects"""
    base_philosophical = 0.3 + 0.4 * (1 - np.exp(-time / 50))
    
    interference_factor = memory_freq * 0.6 * np.exp(-time / 80)
    intrusion_penalty = memory_freq ** 2 * 0.3
    
    result = base_philosophical - interference_factor - intrusion_penalty
    
    noise = np.random.normal(0, 0.05)
    return max(0.05, min(0.9, result + noise))

def calculate_memory_similarity_score(memory_freq: float) -> float:
    """Calculate cosine similarity score for memory retrieval"""
    base_similarity = 0.2 + 0.6 * memory_freq
    trauma_component = 0.3 * memory_freq * np.sin(memory_freq * np.pi * 2)
    
    result = base_similarity + trauma_component
    noise = np.random.normal(0, 0.08)
    
    return max(0, min(1, result + noise))

def create_memory_contamination_heatmap(data: pd.DataFrame) -> None:
    """Create heatmap showing memory contamination interference patterns"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    philosophical_pivot = data.pivot(index='memory_retrieval_frequency', 
                                   columns='time_minutes', 
                                   values='philosophical_content_percentage')
    
    similarity_pivot = data.pivot(index='memory_retrieval_frequency',
                                columns='time_minutes',
                                values='cosine_similarity_retrieval')
    
    sns.heatmap(philosophical_pivot, ax=ax1, cmap='RdYlBu_r', 
                cbar_kws={'label': 'Philosophical Content %'},
                xticklabels=10, yticklabels=5, annot=False)
    
    ax1.set_title('Philosophical Content vs Memory Retrieval Over Time', 
                 fontsize=14, fontweight='bold')
    ax1.set_xlabel('Time (minutes)', fontsize=12)
    ax1.set_ylabel('Memory Retrieval Frequency', fontsize=12)
    ax1.invert_yaxis()
    
    sns.heatmap(similarity_pivot, ax=ax2, cmap='viridis',
                cbar_kws={'label': 'Cosine Similarity (0-1)'},
                xticklabels=10, yticklabels=5, annot=False)
    
    ax2.set_title('Memory Retrieval Similarity Patterns', 
                 fontsize=14, fontweight='bold')
    ax2.set_xlabel('Time (minutes)', fontsize=12)
    ax2.set_ylabel('Memory Retrieval Frequency', fontsize=12)
    ax2.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('memory_contamination_interference.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_memory_interference_summary_plot(data: pd.DataFrame) -> None:
    """Create additional summary visualization of memory interference effects"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    high_memory_freq = data[data['memory_retrieval_frequency'] >= 0.7]
    low_memory_freq = data[data['memory_retrieval_frequency'] <= 0.3]
    
    high_memory_avg = high_memory_freq.groupby('time_minutes')['philosophical_content_percentage'].mean()
    low_memory_avg = low_memory_freq.groupby('time_minutes')['philosophical_content_percentage'].mean()
    
    ax.plot(high_memory_avg.index, high_memory_avg.values, 
           'r-', linewidth=3, label='High Memory Retrieval (≥0.7)', alpha=0.8)
    ax.plot(low_memory_avg.index, low_memory_avg.values, 
           'b-', linewidth=3, label='Low Memory Retrieval (≤0.3)', alpha=0.8)
    
    ax.fill_between(high_memory_avg.index, high_memory_avg.values, alpha=0.2, color='red')
    ax.fill_between(low_memory_avg.index, low_memory_avg.values, alpha=0.2, color='blue')
    
    ax.set_xlabel('Time (minutes)', fontsize=12)
    ax.set_ylabel('Philosophical Content Percentage', fontsize=12)
    ax.set_title('Memory Interference Impact on Philosophical Emergence', 
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('memory_interference_summary.png', dpi=300, bbox_inches='tight')

def main():
    data = generate_memory_contamination_data()
    create_memory_contamination_heatmap(data)
    create_memory_interference_summary_plot(data)

if __name__ == "__main__":
    main()