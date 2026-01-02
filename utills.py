"""Utility functions and helpers"""

import os
import json
import numpy as np
import torch
from datetime import datetime

class ModelManager:
    """Manage saving and loading model checkpoints"""
    
    def __init__(self, save_dir='models'):
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def save_model(self, agent, episode, stats=None):
        """Save agent model and training stats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"model_ep{episode}_{timestamp}.pt"
        filepath = os.path.join(self.save_dir, filename)
        
        checkpoint = {
            'state_dict': agent.q_network.state_dict(),
            'target_state_dict': agent.target_network.state_dict(),
            'epsilon': agent.epsilon,
            'episode': episode,
            'stats': stats
        }
        
        torch.save(checkpoint, filepath)
        print(f"Model saved: {filepath}")
        
        return filepath
    
    def load_model(self, agent, filepath):
        """Load agent model from checkpoint"""
        checkpoint = torch.load(filepath)
        agent.q_network.load_state_dict(checkpoint['state_dict'])
        agent.target_network.load_state_dict(checkpoint['target_state_dict'])
        agent.epsilon = checkpoint['epsilon']
        
        print(f"Model loaded: {filepath}")
        return checkpoint.get('stats', None)
    
    def save_stats(self, stats, filename='training_stats.json'):
        """Save training statistics"""
        filepath = os.path.join(self.save_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(stats, f, indent=4)
        print(f"Stats saved: {filepath}")


class StatisticsTracker:
    """Track training statistics"""
    
    def __init__(self):
        self.episode_rewards = []
        self.episode_fish_eaten = []
        self.episode_fish_survived = []
        self.episode_steps = []
        self.average_rewards = []
        # per-generation genome statistics
        self.generation_stats = []
    
    def record_episode(self, reward, fish_eaten, steps, fish_survived=None):
        """Record episode statistics"""
        self.episode_rewards.append(reward)
        self.episode_fish_eaten.append(fish_eaten)
        # record survivors if provided
        if fish_survived is not None:
            self.episode_fish_survived.append(fish_survived)
        self.episode_steps.append(steps)
        
        # Calculate moving average
        if len(self.episode_rewards) >= 10:
            avg = np.mean(self.episode_rewards[-10:])
            self.average_rewards.append(avg)
    
    def get_summary(self):
        """Get summary statistics"""
        if not self.episode_rewards:
            return {}
        gen_summary = None
        if self.generation_stats:
            gen_summary = self.generation_stats[-1]
        return {
            'total_episodes': len(self.episode_rewards),
            'avg_reward': np.mean(self.episode_rewards),
            'max_reward': max(self.episode_rewards),
            'min_reward': min(self.episode_rewards),
            'total_fish_eaten': sum(self.episode_fish_eaten),
            'total_fish_survived': int(np.sum(self.episode_fish_survived)) if self.episode_fish_survived else 0,
            'avg_steps': np.mean(self.episode_steps)
        }
    
    def print_summary(self):
        """Print summary to console"""
        summary = self.get_summary()
        if summary:
            print("\n=== Training Summary ===")
            for key, value in summary.items():
                if isinstance(value, float):
                    print(f"{key}: {value:.2f}")
                else:
                    print(f"{key}: {value}")
            print("=======================\n")

    def record_generation(self, generation, genomes):
        """Record summary statistics for a generation's genomes.

        `genomes` is expected to be a list of genome dicts (or objects with numeric fields).
        """
        if not genomes:
            return

        # collect numeric fields
        keys = ['perception_radius', 'panic_multiplier', 'flee_speed', 'max_speed', 'steering_smoothness']
        stats = {'generation': generation, 'n': len(genomes)}
        for k in keys:
            vals = [float(g.get(k, 0.0)) if isinstance(g, dict) else float(getattr(g, k, 0.0)) for g in genomes]
            stats[f'{k}_mean'] = float(np.mean(vals))
            stats[f'{k}_median'] = float(np.median(vals))
            stats[f'{k}_min'] = float(np.min(vals))
            stats[f'{k}_max'] = float(np.max(vals))

        self.generation_stats.append(stats)
        # Convenience printout when verbose
        try:
            print(f"Gen {generation}: n={stats['n']} | flee_speed_mean={stats['flee_speed_mean']:.2f} | perception_mean={stats['perception_radius_mean']:.1f}")
        except Exception:
            pass


class ActionMapper:
    """Map discrete actions to continuous movements"""
    
    ACTIONS = {
        0: {'vx': 0, 'vy': -3, 'name': 'UP'},
        1: {'vx': 0, 'vy': 3, 'name': 'DOWN'},
        2: {'vx': -3, 'vy': 0, 'name': 'LEFT'},
        3: {'vx': 3, 'vy': 0, 'name': 'RIGHT'},
    }
    
    @staticmethod
    def get_velocity(action):
        """Get velocity from action"""
        return ActionMapper.ACTIONS[action]
    
    @staticmethod
    def get_action_name(action):
        """Get human-readable action name"""
        return ActionMapper.ACTIONS[action]['name']


class RollingAverage:
    """Calculate rolling average of values"""
    
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.values = []
    
    def add(self, value):
        """Add value to rolling window"""
        self.values.append(value)
        if len(self.values) > self.window_size:
            self.values.pop(0)
    
    def get_average(self):
        """Get current average"""
        if not self.values:
            return 0
        return np.mean(self.values)