

width = 800
height = 600

fps = 60

title = "fish and ball"

#game properties
numFish = 10
NumBall =1

#ball properties
ballRadius = 12
ballSpeed = 5

# Fish Properties
fishSize = 6
fishMinSpeed = -2
fishMaxSpeed = 2
fishDirectionChangeMin = 30
fishDirectionChangeMax = 100

# Agent Properties
stateSize = 8
actionSize = 4
learningRate = 0.001
memorySize = 2000
batchSize = 32

# DQN Parameters
gamma = 0.95  # Discount factor
epsilonStart = 1.0
epsilonMin = 0.01
epsilonDecay = 0.995
targetUpdateFrequency = 0.01

# Reward Settings (Fixed - assuming these are for FISH agents)
rewardSurvival = 0.01
rewardEaten = -10  # Changed from REWARD_EAT_FISH to REWARD_EATEN
rewardDistanceMultiplier = 1.0
rewardBoundaryPenalty = 0

# Display Settings
colorBackground = (30, 30, 30)
colorBall = (255, 100, 100)
colorFish = (100, 150, 255)
colorText = (255, 255, 255)
fontSize = 36

# Training Settings
saveModelEveryNEpisodes = 50
renderGame = True
verbose = True