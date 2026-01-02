import pygame
import config

class Renderer:
    """Screen initialization and rendering"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(config.TITLE)
        
        # Initialize fonts for UI text
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

    
    def draw_fish(self, fish_list):
        """Draw all fish as triangles"""
        for fish in fish_list:
            pygame.draw.polygon(self.screen, config.COLOR_FISH, fish.get_points())


    def draw_ball(self, ball):
        """Draw the ball"""
        pygame.draw.circle(self.screen, config.COLOR_BALL, ball.get_position(), ball.radius)

    
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

    #render function
    def render(self, fish_list, ball, episode, steps, reward, fish_eaten):
        """Main rendering function"""
        self.screen.fill(config.COLOR_BACKGROUND)
        self.draw_fish(fish_list)
        self.draw_ball(ball)
        self._draw_ui(episode, steps, reward, fish_eaten)
        pygame.display.flip()