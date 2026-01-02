


# Window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
TITLE = "fish and ball"

# Game properties
NUM_FISH = 10

# Ball properties
BALL_RADIUS = 28
BALL_SPEED = 4
BALL_MAX_SPEED = 6

# Fish properties
FISH_SIZE = 18
FISH_MIN_SPEED = -2
FISH_MAX_SPEED = 5
FISH_DIRECTION_CHANGE_MIN = 30
FISH_DIRECTION_CHANGE_MAX = 100

# Agent / DQN
STATE_SIZE = 8
ACTION_SIZE = 4
LEARNING_RATE = 0.001
MEMORY_SIZE = 2000
BATCH_SIZE = 32
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995
TARGET_UPDATE_FREQUENCY = 0.01

# Rewards
REWARD_SURVIVAL = 0.01
REWARD_EATEN = 10
REWARD_DISTANCE_MULTIPLIER = 1.0
REWARD_BOUNDARY_PENALTY = 0

# Display
COLOR_BACKGROUND = (30, 30, 30)
COLOR_BALL = (255, 100, 100)
COLOR_FISH = (100, 150, 255)
COLOR_TEXT = (255, 255, 255)
FONT_SIZE = 36

# Training / Misc
SAVE_MODEL_EVERY_N_EPISODES = 50
RENDER_GAME = True
VERBOSE = True
# Ball assist and growth
BALL_AUTO_CHASE = True
# Moderate chase strength so fish have a chance to flee
BALL_CHASE_STRENGTH = 0.6 # steering blend (0-1)
BALL_GROW_ON_EAT = False
BALL_GROW_AMOUNT = 2  # pixels added to radius per eaten fish
BALL_MAX_RADIUS = 200

# Fish flee behavior
FLEE_DISTANCE = 100
FLEE_SPEED = 2.5

# Fish learning parameters (per-episode adaptation)
FLEE_LEARNING_RATE = 0.0010  # fraction by which flee speed can increase per successful generation
FLEE_MIN_SPEED = 1.0
FLEE_MAX_SPEED = 6.0

# Improved fish avoidance tunables
FLEE_DISTANCE = 140  # detection radius for fleeing
FISH_MAX_SPEED = 5.0
FISH_ACCEL = 0.45    # how quickly a fish can change velocity toward desired flee vector
PANIC_MULTIPLIER = 1.5  # extra speed multiplier when ball is heading toward fish
PREDICTION_TIME = 0.5    # seconds ahead to predict ball position for evasive maneuvers

# Evolutionary per-fish learning
FISH_MUTATION_RATE = 0.3
FISH_MUTATION_SCALE = 0.5  # standard deviation for Gaussian mutation

# Evolution and genome tuning
FISH_GENOME_ELITISM = 2        # number of top genomes preserved unchanged each generation
FISH_TOURNAMENT_SIZE = 3       # tournament size for selection
FISH_MUTATION_DECAY = 0.995   # per-generation multiplier for mutation scale

# Genome parameter bounds
FISH_PERCEPTION_MIN = 50
FISH_PERCEPTION_MAX = 220
FISH_PANIC_MIN = 0.5
FISH_PANIC_MAX = 3.0
FISH_STEERING_MIN = 0.05
FISH_STEERING_MAX = 1.0

# Fitness weighting (how to combine survival + distance)
FISH_FITNESS_DISTANCE_WEIGHT = 0.5
FISH_FITNESS_SURVIVAL_WEIGHT = 1.0