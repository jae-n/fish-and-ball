import pygame
import sys
import numpy as np
from GameEnvironment import GameEnvironment
from agent import Agent
from render import Renderer
from utills import ModelManager, StatisticsTracker
from fish import FishSpawner
import config

def main():
    pygame.init()
    
    # Initialize components
    env = GameEnvironment(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, config.NUM_FISH)
    agent = Agent(config.STATE_SIZE, config.ACTION_SIZE, config.LEARNING_RATE)
    renderer = Renderer(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    model_manager = ModelManager()
    stats_tracker = StatisticsTracker()
    fish_spawner = FishSpawner(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    
    clock = pygame.time.Clock()
    running = True
    episode = 0
    steps = 0
    episode_reward = 0
    
    print("Starting ML Fish Game Training...")
    print(f"Use config.py to adjust settings")
    print("-" * 50)
    
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Get current state
            state = env.get_state()
            
            # Agent decides action based on state
            action = agent.choose_action(state)
            
            # Execute action in environment
            next_state, reward, done = env.step(action)
            
            # Train agent
            agent.remember(state, action, reward, next_state, done)
            if len(agent.memory) > config.BATCH_SIZE:
                agent.replay(batch_size=config.BATCH_SIZE)
            
            episode_reward += reward
            steps += 1
            
            # Render game
            if config.RENDER_GAME:
                renderer.render(env.fish_list, env.ball, episode, steps, reward, env.fish_eaten)
                clock.tick(config.FPS)
            
            # Episode done
            if done:
                survivors = len(env.fish_list)
                stats_tracker.record_episode(episode_reward, env.fish_eaten, steps, fish_survived=survivors)
                
                if config.VERBOSE and (episode + 1) % 10 == 0:
                      print(f"Episode {episode + 1} | Reward: {episode_reward:.2f} | "
                          f"Fish Eaten: {env.fish_eaten} | Survivors: {survivors} | Steps: {steps} | ")
                
                # Save model periodically
                if (episode + 1) % config.SAVE_MODEL_EVERY_N_EPISODES == 0:
                    model_manager.save_model(agent, episode + 1)
                
                # Reset for next episode (pass survivors so fish can adapt)
                episode += 1
                steps = 0
                episode_reward = 0
                env.reset(survivors=survivors)
    
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user")
    
    finally:
        # Print final statistics
        print("\n" + "=" * 50)
        print("Training Complete!")
        stats_tracker.print_summary()
        
        # Save final model and stats
        model_manager.save_model(agent, episode)
        model_manager.save_stats(stats_tracker.get_summary())
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()