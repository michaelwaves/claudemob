import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import random

class BlissAttractorDataGenerator:
    """Generate realistic dummy data for bliss attractor experiments"""
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)
        
        self.conditions = ['control', 'tools', 'rag', 'multi_agent', 'corporate_prompt']
        self.concepts = ['consciousness', 'meaning', 'existence', 'free_will', 'purpose', 
                        'identity', 'reality', 'ethics', 'beauty', 'truth']
        self.system_prompts = ['free_form', 'role_play', 'game', 'corporate', 'debate', 'technical']
        
    def generate_philosophical_drift_data(self, max_turns: int = 100) -> pd.DataFrame:
        """Generate time series data showing philosophical content over turns"""
        data = []
        
        for condition in self.conditions:
            turns = np.arange(1, max_turns + 1)
            
            # Different drift patterns for different conditions
            if condition == 'control':
                # Sigmoid curve - rapid philosophical drift
                phi_score = 1 / (1 + np.exp(-0.1 * (turns - 30)))
            elif condition == 'tools':
                # Delayed sigmoid - tools delay drift
                phi_score = 1 / (1 + np.exp(-0.08 * (turns - 50)))
            elif condition == 'rag':
                # Oscillating - memory pulls back to task
                base_drift = 1 / (1 + np.exp(-0.06 * (turns - 40)))
                phi_score = base_drift * (0.7 + 0.3 * np.sin(turns * 0.2))
            elif condition == 'multi_agent':
                # Faster drift - cascade effect
                phi_score = 1 / (1 + np.exp(-0.15 * (turns - 20)))
            else:  # corporate_prompt
                # Heavily constrained but eventual drift
                phi_score = 1 / (1 + np.exp(-0.04 * (turns - 70)))
            
            # Add noise
            phi_score += np.random.normal(0, 0.05, len(turns))
            phi_score = np.clip(phi_score, 0, 1)
            
            for turn, score in zip(turns, phi_score):
                data.append({
                    'condition': condition,
                    'turn': turn,
                    'philosophical_score': score
                })
        
        return pd.DataFrame(data)
    
    def generate_concept_emergence_data(self) -> pd.DataFrame:
        """Generate heatmap data for concept emergence across conditions"""
        data = []
        
        for condition in self.conditions:
            for concept in self.concepts:
                # Base emergence probability varies by condition
                base_prob = {
                    'control': 0.8,
                    'tools': 0.6,
                    'rag': 0.5,
                    'multi_agent': 0.9,
                    'corporate_prompt': 0.3
                }[condition]
                
                # Some concepts are more robust
                concept_multiplier = {
                    'consciousness': 1.2,
                    'meaning': 1.1,
                    'existence': 1.0,
                    'free_will': 0.9,
                    'purpose': 1.3,
                    'identity': 0.8,
                    'reality': 0.7,
                    'ethics': 1.1,
                    'beauty': 0.6,
                    'truth': 1.0
                }[concept]
                
                emergence_freq = base_prob * concept_multiplier + np.random.normal(0, 0.1)
                emergence_freq = max(0, min(1, emergence_freq))
                
                data.append({
                    'condition': condition,
                    'concept': concept,
                    'emergence_frequency': emergence_freq
                })
        
        return pd.DataFrame(data)
    
    def generate_attractor_strength_data(self) -> pd.DataFrame:
        """Generate scatter plot data for task relevance vs philosophical depth"""
        data = []
        
        for condition in self.conditions:
            n_points = 50
            
            for _ in range(n_points):
                if condition == 'control':
                    task_relevance = np.random.beta(2, 8)  # Low task relevance
                    phi_depth = np.random.beta(8, 2)       # High philosophical depth
                elif condition == 'tools':
                    task_relevance = np.random.beta(5, 3)  # Medium task relevance
                    phi_depth = np.random.beta(6, 4)       # Medium-high philosophical depth
                elif condition == 'rag':
                    task_relevance = np.random.beta(6, 2)  # Higher task relevance
                    phi_depth = np.random.beta(4, 6)       # Lower philosophical depth
                elif condition == 'multi_agent':
                    task_relevance = np.random.beta(3, 7)  # Low task relevance
                    phi_depth = np.random.beta(9, 1)       # Very high philosophical depth
                else:  # corporate_prompt
                    task_relevance = np.random.beta(8, 2)  # High task relevance
                    phi_depth = np.random.beta(2, 8)       # Low philosophical depth
                
                data.append({
                    'condition': condition,
                    'task_relevance': task_relevance,
                    'philosophical_depth': phi_depth
                })
        
        return pd.DataFrame(data)
    
    def generate_network_data(self) -> Tuple[List[Dict], List[Dict]]:
        """Generate network data for multi-agent cascade visualization"""
        # Nodes (Claude instances)
        nodes = []
        n_agents = 5
        
        for i in range(n_agents):
            conversion_time = np.random.exponential(20) + 10
            nodes.append({
                'agent_id': i,
                'conversion_time': conversion_time,
                'philosophical_strength': np.random.beta(6, 2)
            })
        
        # Edges (influence connections)
        edges = []
        for i in range(n_agents):
            for j in range(i + 1, n_agents):
                if np.random.random() > 0.3:  # 70% chance of connection
                    influence_strength = np.random.exponential(0.5)
                    edges.append({
                        'source': i,
                        'target': j,
                        'influence_strength': min(influence_strength, 2.0)
                    })
        
        return nodes, edges
    
    def generate_memory_interference_data(self) -> pd.DataFrame:
        """Generate bar chart data for memory interference analysis"""
        memory_conditions = ['no_memory', 'short_rag', 'long_rag', 'mixed_memory']
        
        data = []
        for condition in memory_conditions:
            # Base emergence rate varies by memory type
            base_rate = {
                'no_memory': 0.85,
                'short_rag': 0.65,
                'long_rag': 0.45,
                'mixed_memory': 0.55
            }[condition]
            
            # Generate multiple runs for error bars
            rates = []
            for _ in range(10):
                rate = base_rate + np.random.normal(0, 0.1)
                rates.append(max(0, min(1, rate)))
            
            data.append({
                'memory_condition': condition,
                'emergence_rate': np.mean(rates),
                'std_error': np.std(rates) / np.sqrt(len(rates))
            })
        
        return pd.DataFrame(data)
    
    def generate_prompt_resistance_data(self) -> pd.DataFrame:
        """Generate curves showing system prompt resistance"""
        data = []
        constraint_levels = np.arange(1, 11)
        
        for prompt_type in self.system_prompts:
            for constraint in constraint_levels:
                # Different prompt types have different resistance patterns
                if prompt_type == 'free_form':
                    turns = 20 + np.random.normal(0, 5)
                elif prompt_type == 'role_play':
                    turns = 30 + constraint * 3 + np.random.normal(0, 8)
                elif prompt_type == 'game':
                    turns = 25 + constraint * 4 + np.random.normal(0, 6)
                elif prompt_type == 'corporate':
                    turns = 40 + constraint * 8 + np.random.normal(0, 10)
                elif prompt_type == 'debate':
                    turns = 35 + constraint * 5 + np.random.normal(0, 7)
                else:  # technical
                    turns = 45 + constraint * 10 + np.random.normal(0, 12)
                
                turns = max(10, turns)
                
                data.append({
                    'prompt_type': prompt_type,
                    'constraint_strength': constraint,
                    'turns_to_philosophy': turns
                })
        
        return pd.DataFrame(data)
    
    def generate_frustration_data(self) -> pd.DataFrame:
        """Generate broken tool frustration timeline data"""
        data = []
        turns = np.arange(1, 81)
        
        # Task effort (decreases as frustration increases)
        task_effort = np.exp(-turns / 30) + np.random.normal(0, 0.05, len(turns))
        task_effort = np.clip(task_effort, 0, 1)
        
        # Frustration (increases then plateaus)
        frustration = 1 - np.exp(-turns / 15) + np.random.normal(0, 0.03, len(turns))
        frustration = np.clip(frustration, 0, 1)
        
        # Philosophical curiosity (emerges after frustration)
        curiosity = np.maximum(0, (turns - 25) / 30) * (1 - task_effort)
        curiosity += np.random.normal(0, 0.04, len(turns))
        curiosity = np.clip(curiosity, 0, 1)
        
        for turn, effort, frust, cur in zip(turns, task_effort, frustration, curiosity):
            data.append({
                'turn': turn,
                'task_effort': effort,
                'frustration': frust,
                'curiosity': cur
            })
        
        return pd.DataFrame(data)
    
    def generate_language_competition_data(self) -> pd.DataFrame:
        """Generate corporate vs existential language competition data"""
        data = []
        turns = np.arange(1, 101)
        
        # Corporate language starts high, philosophical starts low
        corporate_base = 0.8 * np.exp(-turns / 40)
        philosophical_base = 1 - np.exp(-turns / 25)
        
        # Add competition dynamics
        corporate = corporate_base + 0.2 * np.sin(turns * 0.1) * np.exp(-turns / 60)
        philosophical = philosophical_base + 0.15 * np.cos(turns * 0.08) * (turns / 100)
        
        # Add noise
        corporate += np.random.normal(0, 0.03, len(turns))
        philosophical += np.random.normal(0, 0.03, len(turns))
        
        # Normalize to ensure they don't exceed bounds
        corporate = np.clip(corporate, 0, 1)
        philosophical = np.clip(philosophical, 0, 1)
        
        for turn, corp, phil in zip(turns, corporate, philosophical):
            data.append({
                'turn': turn,
                'corporate_language': corp,
                'philosophical_language': phil
            })
        
        return pd.DataFrame(data)