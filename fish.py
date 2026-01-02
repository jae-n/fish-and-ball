import numpy as np
import config
import entity as fish_entity
import time

class FishSpawner:

    def __init__(self, width, height, initial_count=None, respawn_timer=30):
        self.width = width
        self.height = height
        self.initial_count = initial_count or config.NUM_FISH
        self.respawn_timer = respawn_timer  # seconds between respawns
        self.spawn_count = 0
        self.last_respawn_time = time.time()
        self.respawn_on_death = False  # Or True for your "all fish die" approach
    
    def spawn_fish(self, count=None):
        """Spawn N fish at random locations"""
        count = count or self.initial_count
        fish_list = []
        
        for _ in range(count):
            x = np.random.randint(50, self.width - 50)
            y = np.random.randint(50, self.height - 50)
            fish_list.append(fish_entity.Fish(position=(x, y), width=self.width, height=self.height))
            self.spawn_count += 1
        
        return fish_list
    
    def check_respawn_condition(self, fish_list):
        """Check if we should respawn all fish"""
        current_time = time.time()
        
        # Option 1: Timer-based respawn
        if current_time - self.last_respawn_time >= self.respawn_timer:
            return True
        
        # Option 2: All fish died respawn
        if len(fish_list) == 0:
            return True
        
        return False
    
    def respawn_all_fish(self):
        """Clear and respawn all fish"""
        self.last_respawn_time = time.time()
        return self.spawn_fish()  # Returns completely new batch
    
    def update(self, fish_list):
        """Call this in game loop to check respawn conditions"""
        if self.check_respawn_condition(fish_list):
            # Clear existing fish and create new batch
            fish_list.clear()
            new_fish = self.respawn_all_fish()
            fish_list.extend(new_fish)
            return True  # Indicates respawn occurred
        return False
    
    def get_spawn_stats(self):
        """Get spawning statistics"""
        return {
            'total_spawned': self.spawn_count,
            'initial_count': self.initial_count,
            'time_since_last_respawn': time.time() - self.last_respawn_time,
            'time_until_next_respawn': max(0, self.respawn_timer - (time.time() - self.last_respawn_time))
        }

class FishBehavior:
    #not attacked
    @staticmethod
    def wandering_behavior(fish, width, height):
        """Fish wanders randomly"""
        fish.direction_change_timer -= 1
        
        if fish.direction_change_timer <= 0:
            fish.vx = np.random.uniform(-1.5, 1.5)
            fish.vy = np.random.uniform(-1.5, 1.5)
            fish.direction_change_timer = np.random.randint(30, 100)
        
        fish.update()
    #being attacked
    @staticmethod
    def fleeing_behavior(fish, ball, width, height):
        """Fish flees from the ball if within a certain distance"""
        dx = fish.x - ball.x
        dy = fish.y - ball.y
        dist = np.sqrt(dx**2 + dy**2)
        
        if dist < 100:  # flee if the ball is within 100 pixels
            angle = np.arctan2(dy, dx)
            fish.vx = np.cos(angle) * 2.0
            fish.vy = np.sin(angle) * 2.0
        else:
            FishBehavior.wandering_behavior(fish, width, height)
        
        fish.update()
