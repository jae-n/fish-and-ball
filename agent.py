import numpy as np
import torch
import config
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random

# caluation of q 
class DQNAgent (nn.Module):
    def __init__(self,state_size, action_size):
        super(DQNAgent, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)
        
    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)
    
class Agent:
    #: Stores past experiences
    def __init__(self, state_size, action_size, learning_rate=0.001):
            self.state_size = state_size
            self.action_size = action_size
            self.memory = deque(maxlen=2000)
            
            # Exploration rate
            self.epsilon = 1.0
            self.epsilon_min = 0.01
            self.epsilon_decay = 0.995
            
            # Discount factor
            self.gamma = 0.95
            self.learning_rate = learning_rate
            
            # Neural networks
            
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            #main network
            self.q_network = DQNAgent(state_size, action_size).to(self.device)
             # Target network
            self.target_network = DQNAgent(state_size, action_size).to(self.device)
            #copy weights from main to target
            self.target_network.load_state_dict(self.q_network.state_dict())
            
            self.optimizer = optim.Adam(self.q_network.parameters(), lr=learning_rate)
            self.loss_fn = nn.MSELoss()


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        #start with random action for exploration
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        
        # the next best action based on q values
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.q_network(state)
        return torch.argmax(q_values).item()

    # Backwards-compatible API: some modules expect `choose_action`
    def choose_action(self, state):
        return self.act(state)
    
    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        #start training with random samples from memory
        minibatch = random.sample(self.memory, batch_size)
        
        #get batches information
        states = torch.FloatTensor([experience[0] for experience in minibatch]).to(self.device)
        actions = torch.LongTensor([experience[1] for experience in minibatch]).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor([experience[2] for experience in minibatch]).to(self.device)
        next_states = torch.FloatTensor([experience[3] for experience in minibatch]).to(self.device)
        dones = torch.FloatTensor([float(experience[4]) for experience in minibatch]).to(self.device)
        
        # Current Q values
        q_values = self.q_network(states).gather(1, actions).squeeze()
        
        # Target Q values
        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(1)[0]
            target_q_values = rewards + (self.gamma * next_q_values * (1 - dones))
        
        # Compute loss
        loss = self.loss_fn(q_values, target_q_values)
        
        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Soft-update target network towards q_network
        try:
            tau = getattr(config, 'TARGET_UPDATE_FREQUENCY', 0.01)
            for target_param, param in zip(self.target_network.parameters(), self.q_network.parameters()):
                target_param.data.copy_(tau * param.data + (1.0 - tau) * target_param.data)
        except Exception:
            pass

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay