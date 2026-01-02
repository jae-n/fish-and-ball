import numpy as np
import config
#ball entity
class Ball:
    def __init__(self, position, radius, width, height):
        self.x, self.y = position
        self.position = np.array(position)
        self.vx, self.vy = 0, 0
        self.radius = radius
        self.speed = config.BALL_SPEED
        self.width = width
        self.height = height
    #get ball position and update
    def get_position(self):
        self.x += self.vx
        self.y += self.vy

        # Keep ball within screen bounds and reflect velocity
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius > self.width:
            self.x = self.width - self.radius
            self.vx = -abs(self.vx)

        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = abs(self.vy)
        elif self.y + self.radius > self.height:
            self.y = self.height - self.radius
            self.vy = -abs(self.vy)

        # Clamp ball velocity to a configurable maximum speed
        try:
            max_speed = float(config.BALL_MAX_SPEED)
        except Exception:
            max_speed = float(self.speed)

        vel_mag = (self.vx ** 2 + self.vy ** 2) ** 0.5
        if vel_mag > max_speed and vel_mag > 1e-8:
            scale = max_speed / vel_mag
            self.vx *= scale
            self.vy *= scale

        return (int(self.x), int(self.y))
    

    
class Fish:
    def __init__(self, position, width, height, genome=None):
        self.x, self.y = position
        self.width = width
        self.height = height
        self.size = config.FISH_SIZE
        # initial random movement
        self.vx = np.random.uniform(config.FISH_MIN_SPEED, config.FISH_MAX_SPEED)
        self.vy = np.random.uniform(config.FISH_MIN_SPEED, config.FISH_MAX_SPEED)
        self.direction_change_counter = 0
        self.radius = self.size

        # genome: a dict with behavioral parameters
        if genome is None:
            # randomize a genome within configured bounds
            self.genome = {
                'perception_radius': float(np.random.uniform(config.FISH_PERCEPTION_MIN, config.FISH_PERCEPTION_MAX)),
                'panic_multiplier': float(np.random.uniform(config.FISH_PANIC_MIN, config.FISH_PANIC_MAX)),
                'flee_speed': float(np.random.uniform(config.FLEE_MIN_SPEED, config.FLEE_MAX_SPEED)),
                'max_speed': float(np.random.uniform(config.FISH_MAX_SPEED * 0.5, config.FISH_MAX_SPEED)),
                'steering_smoothness': float(np.random.uniform(config.FISH_STEERING_MIN, config.FISH_STEERING_MAX))
            }
        else:
            # copy genome provided
            self.genome = dict(genome)

        # convenience attributes for quick access
        self.perception_radius = float(self.genome.get('perception_radius', config.FLEE_DISTANCE))
        self.panic_multiplier = float(self.genome.get('panic_multiplier', config.PANIC_MULTIPLIER))
        self.flee_speed = float(self.genome.get('flee_speed', config.FLEE_MIN_SPEED))
        self.max_speed = float(self.genome.get('max_speed', config.FISH_MAX_SPEED))
        self.steering_smoothness = float(self.genome.get('steering_smoothness', config.FISH_ACCEL))

        # fitness for evolutionary selection
        self.fitness = 0.0
        # age in steps (how long this fish has survived this episode)
        self.age = 0

    #get fish angle for rendering
    def get_angle(self):
        return np.arctan2(self.vy, self.vx) * 180 / np.pi
    
    #triangle points for fish rendering
    def get_points(self):
        angle = self.get_angle()
        point1 = (self.x + self.size * np.cos(np.radians(angle)),
                  self.y + self.size * np.sin(np.radians(angle)))
        point2 = (self.x + self.size * np.cos(np.radians(angle + 120)),
                  self.y + self.size * np.sin(np.radians(angle + 120)))
        point3 = (self.x + self.size * np.cos(np.radians(angle + 240)),
                  self.y + self.size * np.sin(np.radians(angle + 240)))
        return [point1, point2, point3]
    

    #update fish position and handle boundary collisions
    def update_position(self):
        self.x += self.vx
        self.y += self.vy

        self.direction_change_counter += 1

        if self.direction_change_counter >= np.random.randint(config.FISH_DIRECTION_CHANGE_MIN, config.FISH_DIRECTION_CHANGE_MAX):
            self.vx = np.random.uniform(config.FISH_MIN_SPEED, config.FISH_MAX_SPEED)
            self.vy = np.random.uniform(config.FISH_MIN_SPEED, config.FISH_MAX_SPEED)
            self.direction_change_counter = 0


        #collision with boundaries
        if self.x - self.radius < 0 or self.x + self.radius > self.width:
            self.vx = -self.vx
            self.x = np.clip(self.x, self.radius, self.width - self.radius)
        if self.y - self.radius < 0 or self.y + self.radius > self.height:
            self.vy = -self.vy
            self.y = np.clip(self.y, self.radius, self.height - self.radius)

