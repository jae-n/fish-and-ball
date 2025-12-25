import pygame
import config
import numpy as np
import entity as entity

class GameEnvironment:
    def __init__(self, width, height,num_fish):

        self.width = width
        self.height = height
        self.num_fish = num_fish
        self.fish_list = []
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(config.title)

        self.ball = entity.Ball(position=(self.width // 2, self.height // 2), radius=config.ballRadius) 
        self.fish_list = [entity.Fish(position=(np.random.randint(0, self.width), np.random.randint(0, self.height)),
                                      width=self.width, height=self.height) for _ in range(self.num_fish)]
        
        self.steps = 0
        self.Max_steps = 1000
        self.reward = 0
        self.fish_eaten = 0


    def reset(self):
        self.ball = entity.Ball(position=(self.width // 2, self.height // 2), radius=config.ballRadius) 
        self.fish_list = [entity.Fish(position=(np.random.randint(0, self.width), np.random.randint(0, self.height)),
                                      width=self.width, height=self.height) for _ in range(self.num_fish)]
        self.steps = 0
        self.reward = 0
        self.fish_eaten = 0

    def get_state(self):
        #get the ball state
        ball_x, ball_y = self.ball.get_position()
        state = [ball_x / self.width, ball_y / self.height] 
        
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
            len(self.fish) / self.num_fish
        ], dtype=np.float32)
        
        return state