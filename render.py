import pygame
import config

class Render:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(config.title)



    
    def draw_fish(self, fish_list):
        for fish in fish_list:
            pygame.draw.polygon(self.screen, config.colorFish, fish.get_points())


    def draw_ball(self, ball):
        pygame.draw.circle(self.screen, config.BALL_COLOR, ball.get_position(), ball.radius)

    def render(self, fish_list, ball):
        self.screen.fill(config.colorBackground)
        self.draw_fish(fish_list)
        self.draw_ball(ball)
        self.draw_ball(episode, steps, reward, fishEaten)
        pygame.display.flip()

    def _draw_ui(self, episode, steps, reward, fish_eaten):
        """Draw UI text overlays"""
        texts = [
            (f"Episode: {episode}", 10),
            (f"Steps: {steps}", 50),
            (f"Reward: {reward:.2f}", 90),
            (f"Fish Eaten: {fish_eaten}", 130),
        ]
        
        for text, y_offset in texts:
            rendered = self.font_large.render(text, True, config.COLOR_TEXT)
            self.screen.blit(rendered, (10, y_offset))



    def draw_debug_info(self, ball, fish_list):
        """Draw debug information for development"""
        if not fish_list:
            debug_text = "No fish remaining"
        else:
            closest_dist = min(
                ((ball.x - f.x)**2 + (ball.y - f.y)**2)**0.5 for f in fish_list
            )
            debug_text = f"Closest Fish: {closest_dist:.1f}px, Fish Count: {len(fish_list)}"
        
        rendered = self.font_small.render(debug_text, True, config.COLOR_TEXT)
        self.screen.blit(rendered, (10, self.height - 30))