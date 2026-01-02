import numpy as np


class CollisionDetector:
    @staticmethod
    def distance(entity1, entity2):
        """Calculate Euclidean distance between two entities"""
        dx = entity1.x - entity2.x
        dy = entity1.y - entity2.y
        return np.sqrt(dx**2 + dy**2)

    @staticmethod
    def distance_between(x1, y1, x2, y2):
        dx = x1 - x2
        dy = y1 - y2
        return np.sqrt(dx**2 + dy**2)

    @staticmethod
    def circle_collision(entity1, entity2):
        """Check for collision between two circular entities"""
        dist = CollisionDetector.distance(entity1, entity2)
        return dist < (entity1.radius + entity2.radius)

    @staticmethod
    def check_ball_fish_collisions(ball, fish_list):
        """Check collisions between ball and all fish, return list of collided fish"""
        collided = []
        for fish in fish_list:
            if CollisionDetector.circle_collision(ball, fish):
                collided.append(fish)
        return collided

    @staticmethod
    def check_boundary_collision(entity, width, height):
        """Check if entity collides with boundary"""
        left = entity.x - entity.radius < 0
        right = entity.x + entity.radius > width
        top = entity.y - entity.radius < 0
        bottom = entity.y + entity.radius > height

        return {
            'left': left,
            'right': right,
            'top': top,
            'bottom': bottom,
            'any': left or right or top or bottom
        }

    @staticmethod
    def check_fish_fish_collisions(fish_list):
        """Check collisions between all fish, return list of tuples of collided fish"""
        collided_pairs = []
        for i in range(len(fish_list)):
            for j in range(i + 1, len(fish_list)):
                if CollisionDetector.circle_collision(fish_list[i], fish_list[j]):
                    collided_pairs.append((fish_list[i], fish_list[j]))
        return collided_pairs

    @staticmethod
    def resolve_boundary_collision(entity, width, height):
        """Reverse velocity upon boundary collision"""
        collision = CollisionDetector.check_boundary_collision(entity, width, height)

        if collision['left'] or collision['right']:
            entity.vx = -entity.vx
        if collision['top'] or collision['bottom']:
            entity.vy = -entity.vy

    @staticmethod
    def resolve_fish_fish_collision(fish1, fish2):
        """Simple elastic collision resolution between two fish"""
        # Swap velocities
        fish1.vx, fish2.vx = fish2.vx, fish1.vx
        fish1.vy, fish2.vy = fish2.vy, fish1.vy

    @staticmethod
    def closest_fish(ball, fish_list):
        """Return the closest fish to the ball"""
        if not fish_list:
            return None, float('inf')

        closest_fish = min(fish_list, key=lambda f: CollisionDetector.distance(ball, f))
        closest_dist = CollisionDetector.distance(ball, closest_fish)

        return closest_fish, closest_dist

    @staticmethod
    def get_all_fish_distances(ball_x, ball_y, fish_list):
        """Return distances to all fish"""
        distances = []
        for fish in fish_list:
            dist = CollisionDetector.distance_between(ball_x, ball_y, fish.x, fish.y)
            distances.append(dist)
        return distances