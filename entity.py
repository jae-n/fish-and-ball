import numpy as np
import config

class Ball:
    def __init__(self, position, radius):
        self.x, self.y = position
        self.position = np.array(position)
        self.vx, self.vy = 0, 0
        self.radius = config.BALL_RADIUS
        self.speed = config.BALL_SPEED
        
    def get_position(self):
        self.x +=self.vx
        self.y +=self.vy

        if self.x - self.radius < 0 or self.x + self.radius > config.width:
            self.vx = -self.vx
        if self.y - self.radius < 0 or self.y + self.radius > config.height:
            self.vy = -self.vy
        
        return (int(self.x), int(self.y))
    

    
class Fish:
    def __init__(self, position, width, height):
        self.x, self.y = position
        self.width = width
        self.height = height
        self.size = config.fishSize
        self.vx = np.random.uniform(config.fishMinSpeed, config.fishMaxSpeed)
        self.vy = np.random.uniform(config.fishMinSpeed, config.fishMaxSpeed )  
        self.direction_change_counter = 0

    def get_angle(self):
        return np.arctan2(self.vy, self.vx) * 180 / np.pi
    

    def get_points(self):
        angle = self.get_angle()
        point1 = (self.x + self.size * np.cos(np.radians(angle)),
                  self.y + self.size * np.sin(np.radians(angle)))
        point2 = (self.x + self.size * np.cos(np.radians(angle + 120)),
                  self.y + self.size * np.sin(np.radians(angle + 120)))
        point3 = (self.x + self.size * np.cos(np.radians(angle + 240)),
                  self.y + self.size * np.sin(np.radians(angle + 240)))
        return [point1, point2, point3]
    
    def update_position(self):
        self.x += self.vx
        self.y += self.vy

        self.direction_change_counter += 1

        if self.direction_change_counter >= np.random.randint(config.fishDirectionChangeMin, config.fishDirectionChangeMax):
            self.vx = np.random.uniform(config.fishMinSpeed, config.fishMaxSpeed)
            self.vy = np.random.uniform(config.fishMinSpeed, config.fishMaxSpeed)
            self.direction_change_counter = 0


        #collision with boundaries
        if self.x - self.radius < 0 or self.x + self.radius > self.width:
            self.vx = -self.vx
            self.x = np.clip(self.x, self.radius, self.width - self.radius)
        if self.y - self.radius < 0 or self.y + self.radius > self.height:
            self.vy = -self.vy
            self.y = np.clip(self.y, self.radius, self.height - self.radius)

