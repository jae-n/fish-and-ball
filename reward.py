import numpy as np
from collision_detector import CollisionDetector
import config


class RewardCalculator:
    def __init__(self):
        self.total_reward = 0
        self.fish_eaten_count = 0
        self.max_distance_achieved = 0

    def calculate_reward(self, ball, fish_list, fish_eaten_this_step, 
                    step_count, max_steps, initial_fish_count):
    
        reward = 0
        
        # Calculate base survival rewards
        reward += self._calculate_survival_reward(fish_list)
        
        # Apply penalties for eaten fish
        reward += self._calculate_eaten_fish_penalty(fish_eaten_this_step)
        
        # Add bonus for keeping all fish alive
        reward += self._calculate_all_fish_bonus(fish_list, initial_fish_count)
        
        # Add end-game bonus for surviving the full episode
        if self._is_end_of_episode(step_count, max_steps):
            reward += self._calculate_end_game_bonus(fish_list, initial_fish_count)
        
        # Update tracking statistics
        self._update_tracking_stats(fish_list, fish_eaten_this_step)
        
        self.total_reward += reward
        return reward

# helper function 

def _calculate_survival_reward(self, fish_list):
    """Reward for each fish that is still alive"""
    fish_alive = len(fish_list)
    return fish_alive * 0.1  # 0.1 per living fish

def _calculate_eaten_fish_penalty(self, fish_eaten_this_step):
    """Apply penalty for any fish that were eaten this step"""
    if not fish_eaten_this_step:
        return 0
    
    penalty = -5 * len(fish_eaten_this_step)  # -5 per fish eaten
    return penalty

def _calculate_all_fish_bonus(self, fish_list, initial_fish_count):
    """Bonus if all initial fish are still alive"""
    fish_alive = len(fish_list)
    if fish_alive == initial_fish_count:
        return 0.5  # Extra bonus when all fish survive
    return 0

def _calculate_end_game_bonus(self, fish_list, initial_fish_count):
    """Calculate bonus at the end of episode based on survival rate"""
    fish_alive = len(fish_list)
    survival_rate = fish_alive / initial_fish_count
    
    end_bonus = survival_rate * 50  # Base bonus based on survival rate
    
    # Additional huge bonus if all fish survived
    if fish_alive == initial_fish_count:
        end_bonus += 100
    
    return end_bonus

def _is_end_of_episode(self, step_count, max_steps):
    """Check if this is the final step of the episode"""
    return step_count == max_steps - 1

def _update_tracking_stats(self, fish_list, fish_eaten_this_step):
    """Update internal tracking statistics"""
    # Update fish eaten count
    if fish_eaten_this_step:
        self.fish_eaten_count += len(fish_eaten_this_step)
    
    # Track how long fish have been alive (cumulative)
    fish_alive = len(fish_list)
    self.fish_alive_steps += fish_alive
    
    def get_episode_stats(self):
        """Return statistics for the episode"""
        return {
            'total_reward': self.total_reward,
            'fish_eaten': self.fish_eaten_count,
            'max_distance': self.max_distance_achieved,
            'fish_alive_steps': self.fish_alive_steps
        }
    
    def reset(self):
        """Reset for new episode"""
        self.total_reward = 0
        self.fish_eaten_count = 0
        self.max_distance_achieved = 0
        self.fish_alive_steps = 0
    
   