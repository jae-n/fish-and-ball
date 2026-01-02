import pygame
import config
import numpy as np
import entity as entity
from collision_detector import CollisionDetector

class GameEnvironment:
    def __init__(self, width, height, num_fish):

        self.width = width
        self.height = height
        self.num_fish = num_fish
        self.fish_list = []

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(config.TITLE)

        # Pass bounds to Ball so it can handle boundary collisions
        self.ball = entity.Ball(position=(self.width // 2, self.height // 2), radius=config.BALL_RADIUS, width=self.width, height=self.height)

        # generation counter
        self.generation = 0

        # Initialize per-fish genomes (dicts) and create fish from them
        def random_genome():
            return {
                'perception_radius': float(np.random.uniform(config.FISH_PERCEPTION_MIN, config.FISH_PERCEPTION_MAX)),
                'panic_multiplier': float(np.random.uniform(config.FISH_PANIC_MIN, config.FISH_PANIC_MAX)),
                'flee_speed': float(np.random.uniform(config.FLEE_MIN_SPEED, config.FLEE_MAX_SPEED)),
                'max_speed': float(np.random.uniform(config.FISH_MAX_SPEED * 0.5, config.FISH_MAX_SPEED)),
                'steering_smoothness': float(np.random.uniform(config.FISH_STEERING_MIN, config.FISH_STEERING_MAX))
            }

        self.genomes = [random_genome() for _ in range(self.num_fish)]
        self.fish_list = [entity.Fish(position=(np.random.randint(0, self.width), np.random.randint(0, self.height)),
                          width=self.width, height=self.height, genome=self.genomes[i]) for i in range(self.num_fish)]

        # records of dead fish from the last episode: list of {'genome':..., 'age':...}
        self.dead_records = []

        # Give the ball a small initial random velocity so it can start moving/eating
        self.ball.vx = np.random.uniform(-1.0, 1.0) * self.ball.speed
        self.ball.vy = np.random.uniform(-1.0, 1.0) * self.ball.speed

        # Immediately compute reward to handle any initial overlaps
        self.compute_reward()

        self.steps = 0
        self.Max_steps = 1000
        self.reward = 0
        self.fish_eaten = 0


    def reset(self, survivors=None):

        # Build survivors list (genome + fitness) from remaining fish at episode end
        survivors_list = []
        for fish in self.fish_list:
            try:
                survivors_list.append({'genome': dict(fish.genome), 'fitness': float(getattr(fish, 'fitness', 0.0))})
            except Exception:
                pass

        new_genomes = []
        # if no survivors, reinitialize randomly
        if not survivors_list:
            # if we have dead_records from the episode, choose the longest-lived fish
            if self.dead_records:
                # pick the record with max age
                best = max(self.dead_records, key=lambda r: r.get('age', 0))
                chosen_genome = dict(best['genome'])
                for _ in range(self.num_fish):
                    # replicate the longest-surviving genome across the new generation
                    new_genomes.append(dict(chosen_genome))
            else:
                for _ in range(self.num_fish):
                    new_genomes.append({
                        'perception_radius': float(np.random.uniform(config.FISH_PERCEPTION_MIN, config.FISH_PERCEPTION_MAX)),
                        'panic_multiplier': float(np.random.uniform(config.FISH_PANIC_MIN, config.FISH_PANIC_MAX)),
                        'flee_speed': float(np.random.uniform(config.FLEE_MIN_SPEED, config.FLEE_MAX_SPEED)),
                        'max_speed': float(np.random.uniform(config.FISH_MAX_SPEED * 0.5, config.FISH_MAX_SPEED)),
                        'steering_smoothness': float(np.random.uniform(config.FISH_STEERING_MIN, config.FISH_STEERING_MAX))
                    })
        else:
            # sort survivors by fitness descending
            survivors_list.sort(key=lambda x: x['fitness'], reverse=True)

            # Elitism: copy top genomes unchanged
            elitism = min(config.FISH_GENOME_ELITISM, len(survivors_list))
            for i in range(elitism):
                new_genomes.append(dict(survivors_list[i]['genome']))

            # Adaptive mutation scale based on generation
            mutation_scale = config.FISH_MUTATION_SCALE * (config.FISH_MUTATION_DECAY ** max(0, self.generation))

            # fill rest using tournament selection + mutation
            while len(new_genomes) < self.num_fish:
                # tournament selection among survivors
                contestants = np.random.choice(len(survivors_list), size=min(config.FISH_TOURNAMENT_SIZE, len(survivors_list)), replace=False)
                best = None
                best_idx = None
                for c in contestants:
                    if best is None or survivors_list[c]['fitness'] > best:
                        best = survivors_list[c]['fitness']
                        best_idx = c

                parent = dict(survivors_list[best_idx]['genome'])
                child = dict(parent)

                # mutate numeric genome fields
                for k in child.keys():
                    if np.random.rand() < config.FISH_MUTATION_RATE:
                        child[k] = float(child[k] + np.random.normal(0.0, mutation_scale))

                # clamp mutated values to sensible bounds
                child['perception_radius'] = float(np.clip(child.get('perception_radius', config.FLEE_DISTANCE), config.FISH_PERCEPTION_MIN, config.FISH_PERCEPTION_MAX))
                child['panic_multiplier'] = float(np.clip(child.get('panic_multiplier', config.PANIC_MULTIPLIER), config.FISH_PANIC_MIN, config.FISH_PANIC_MAX))
                child['flee_speed'] = float(np.clip(child.get('flee_speed', config.FLEE_MIN_SPEED), config.FLEE_MIN_SPEED, config.FLEE_MAX_SPEED))
                child['max_speed'] = float(np.clip(child.get('max_speed', config.FISH_MAX_SPEED * 0.1), 0.1, config.FISH_MAX_SPEED))
                child['steering_smoothness'] = float(np.clip(child.get('steering_smoothness', config.FISH_ACCEL), config.FISH_STEERING_MIN, config.FISH_STEERING_MAX))

                new_genomes.append(child)

        # set genomes and recreate fish population at random positions
        self.genomes = new_genomes
        self.fish_list = [entity.Fish(position=(np.random.randint(0, self.width), np.random.randint(0, self.height)),
                                      width=self.width, height=self.height, genome=self.genomes[i]) for i in range(self.num_fish)]

        # increment generation counter
        self.generation += 1

        # generation counter incremented; verbose printing removed

        # reset ball
        self.ball = entity.Ball(position=(self.width // 2, self.height // 2), radius=config.BALL_RADIUS, width=self.width, height=self.height)
        # Give the ball a fresh initial velocity on reset
        self.ball.vx = np.random.uniform(-1.0, 1.0) * self.ball.speed
        self.ball.vy = np.random.uniform(-1.0, 1.0) * self.ball.speed

        # Compute reward to clear any immediate overlaps
        self.compute_reward()
        self.steps = 0
        self.reward = 0
        self.fish_eaten = 0
        # clear dead records for the next episode
        self.dead_records = []

    def adapt_fish_behavior(self, survivors):
        
        if self.num_fish <= 0:
            return
        ratio = float(survivors) / float(self.num_fish)
        # increase flee speed proportionally to survivor ratio
        delta = 1.0 + config.FLEE_LEARNING_RATE * ratio
        new_speed = self.flee_speed * delta
        new_speed = max(config.FLEE_MIN_SPEED, min(config.FLEE_MAX_SPEED, new_speed))
        self.flee_speed = new_speed

    def get_state(self):
        # get the ball state (ensure ball position is current)
        ball_x, ball_y = self.ball.get_position()

        ball_vx = self.ball.vx
        ball_vy = self.ball.vy
        min_dist = float('inf')
        closest_fish_x = 0
        closest_fish_y = 0


        # get ball velocity
        for fish in self.fish_list:
            dx = fish.x - ball_x
            dy = fish.y - ball_y
            dist = np.sqrt(dx**2 + dy**2)
            # find closest fish
            if dist < min_dist:
                min_dist = dist
                closest_fish_x = dx
                closest_fish_y = dy

        # normalize fish position
        state = np.array([
            ball_x / self.width,
            ball_y / self.height,
            ball_vx / 5.0,
            ball_vy / 5.0,
            closest_fish_x / self.width,
            closest_fish_y / self.height,
            min_dist / np.sqrt(self.width**2 + self.height**2),
            len(self.fish_list) / self.num_fish
        ], dtype=np.float32)
        
        return state
    def step(self, action):
        #update ball velocity based on action
        if action == 0:  # up
            self.ball.vy = -self.ball.speed
            self.ball.vx = 0
        elif action == 1:  # down
            self.ball.vy = self.ball.speed
            self.ball.vx = 0
        elif action == 2:  # left
            self.ball.vx = -self.ball.speed
            self.ball.vy = 0
        elif action == 3:  # right
            self.ball.vx = self.ball.speed
            self.ball.vy = 0

        # update the fish positions (baseline wandering update)
        for fish in self.fish_list:
            fish.update_position()

        self.steps += 1

        # optional assist: nudge ball toward closest fish (disabled by default)
        if config.BALL_AUTO_CHASE and self.fish_list:
            closest, _ = CollisionDetector.closest_fish(self.ball, self.fish_list)
            if closest is not None:
                dx = closest.x - self.ball.x
                dy = closest.y - self.ball.y
                dist = np.sqrt(dx * dx + dy * dy) + 1e-6
                dir_x = dx / dist
                dir_y = dy / dist

                # desired velocity toward fish
                desired_vx = dir_x * self.ball.speed
                desired_vy = dir_y * self.ball.speed

                # blend current velocity toward desired
                self.ball.vx += (desired_vx - self.ball.vx) * config.BALL_CHASE_STRENGTH
                self.ball.vy += (desired_vy - self.ball.vy) * config.BALL_CHASE_STRENGTH

        # apply movement limits via get_position (clamping / bouncing)
        self.ball.get_position()

        # Fish behavior: predictive fleeing with per-fish genome parameters
        diag = (self.width**2 + self.height**2) ** 0.5
        for fish in list(self.fish_list):
            # age the fish each step
            fish.age = getattr(fish, 'age', 0) + 1
            dx = fish.x - self.ball.x
            dy = fish.y - self.ball.y
            dist = np.sqrt(dx * dx + dy * dy)

            # update fitness: reward survival and distance from ball
            fish.fitness += config.FISH_FITNESS_SURVIVAL_WEIGHT + (dist / (diag + 1e-6)) * config.FISH_FITNESS_DISTANCE_WEIGHT

            if dist < fish.perception_radius:
                # predict where the ball will be shortly
                pred_x = self.ball.x + self.ball.vx * config.PREDICTION_TIME
                pred_y = self.ball.y + self.ball.vy * config.PREDICTION_TIME

                fx = fish.x - pred_x
                fy = fish.y - pred_y
                fdist = np.sqrt(fx * fx + fy * fy)

                if fdist > 1e-6:
                    nx = fx / fdist
                    ny = fy / fdist
                else:
                    nx = np.random.uniform(-1.0, 1.0)
                    ny = np.random.uniform(-1.0, 1.0)

                # compute approach dot to scale panic
                ball_speed = (self.ball.vx**2 + self.ball.vy**2)**0.5
                ball_to_fish_x = fish.x - self.ball.x
                ball_to_fish_y = fish.y - self.ball.y
                approach_dot = 0.0
                if ball_speed > 1e-6:
                    approach_dot = (self.ball.vx * ball_to_fish_x + self.ball.vy * ball_to_fish_y) / (ball_speed * (dist + 1e-6))

                panic = 1.0
                if approach_dot > 0.0:
                    panic += fish.panic_multiplier * approach_dot

                # desired flee velocity using fish-specific flee_speed and panic
                desired_speed = min(fish.flee_speed * panic, fish.max_speed)
                desired_vx = nx * desired_speed
                desired_vy = ny * desired_speed

                # smooth steering using fish-specific steering_smoothness
                fish.vx += (desired_vx - fish.vx) * fish.steering_smoothness
                fish.vy += (desired_vy - fish.vy) * fish.steering_smoothness

                # clamp fish speed to their per-fish max_speed
                fvel = (fish.vx**2 + fish.vy**2)**0.5
                if fvel > fish.max_speed and fvel > 1e-8:
                    s = fish.max_speed / fvel
                    fish.vx *= s
                    fish.vy *= s

                fish.update_position()
            else:
                fish.update_position()

        # Detect collisions: fish attempt to flee but can still be eaten on contact
        collided = CollisionDetector.check_ball_fish_collisions(self.ball, list(self.fish_list))
        eat_reward = 0
        if collided:
            for f in collided:
                if f in self.fish_list:
                    idx = self.fish_list.index(f)
                    # record dead fish info (genome + age) for selection if needed
                    try:
                        rec_genome = dict(self.fish_list[idx].genome)
                        rec_age = int(getattr(self.fish_list[idx], 'age', 0))
                        self.dead_records.append({'genome': rec_genome, 'age': rec_age})
                    except Exception:
                        pass
                    # remove fish and corresponding genome
                    self.fish_list.pop(idx)
                    try:
                        self.genomes.pop(idx)
                    except Exception:
                        pass
                    self.fish_eaten += 1
                    eat_reward += config.REWARD_EATEN
                    if config.BALL_GROW_ON_EAT:
                        self.ball.radius = min(config.BALL_MAX_RADIUS, self.ball.radius + config.BALL_GROW_AMOUNT)

        # compute remaining reward components (distance/survival)
        reward = self.compute_reward() + eat_reward

        done = self.steps >= self.Max_steps or len(self.fish_list) == 0

        return self.get_state(), reward, done
    

    
    def compute_reward(self):
        # compute distance-based and survival reward (does NOT remove fish)
        reward = config.REWARD_SURVIVAL
        ball_x, ball_y = self.ball.get_position()
        for fish in self.fish_list:
            dx = fish.x - ball_x
            dy = fish.y - ball_y
            dist = np.sqrt(dx**2 + dy**2)
            reward += config.REWARD_DISTANCE_MULTIPLIER / (dist + 1e-5)
        self.reward = reward
        return reward
    

    #get the initial rendering of the game
    def render(self):
        self.screen.fill(config.COLOR_BACKGROUND)

        # Draw ball
        pygame.draw.circle(self.screen, config.COLOR_BALL,
                           (int(self.ball.x), int(self.ball.y)),
                           self.ball.radius)

        # Draw fish
        for fish in self.fish_list:
            pygame.draw.circle(self.screen, config.COLOR_FISH,
                              (int(fish.x), int(fish.y)),
                              fish.radius)
