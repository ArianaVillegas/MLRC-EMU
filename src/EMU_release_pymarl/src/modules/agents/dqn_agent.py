import random
import collections
from copy import deepcopy
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
#nano MLRC-EMU/src/EMU_release_pymarl/src/modules/agents/dqn_agent.py

class ReplayBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = collections.deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = map(np.array, zip(*batch))
        return states, actions, rewards, next_states, dones
    
    def __len__(self):
        return len(self.buffer)

class DQNAgent(nn.Module):
    def __init__(self, obs_dim, action_dim, config):
        super(DQNAgent, self).__init__()
        self.obs_dim = obs_dim
        self.action_dim = action_dim
        print(f"obs_dim: {obs_dim}, action_dim: {action_dim}") 

        '''
        self.gamma = config.get("gamma", 0.99)
        self.lr = config.get("lr", 0.001)
        self.buffer_capacity = config.get("buffer_capacity", 10000)
        self.batch_size = config.get("batch_size", 32)
        '''
        self.gamma = getattr(config, "gamma", 0.99)
        self.lr = getattr(config, "lr", 0.001)
        self.buffer_capacity = getattr(config, "buffer_capacity", 10000)
        self.batch_size = getattr(config, "batch_size", 32)
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.replay_buffer = ReplayBuffer(self.buffer_capacity)
        self.q_network = nn.Sequential(
            nn.Linear(obs_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        ).to(self.device)
        self.target_network = deepcopy(self.q_network)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.lr)

    def init_hidden(self):
        return torch.zeros(1, self.action_dim)

    # 5 por los estados que estan en startcraft2_EMU
    def act(self, state, epsilon=0.1):
        if random.random() < epsilon:
            #return random.randint(0, self.action_dim - 1)
            return random.randint(1, 5 - 1)
        else:
            state_tensor = torch.tensor(state, dtype=torch.float32).to(self.device).unsqueeze(0)
            with torch.no_grad():
                q_values = self.q_network(state_tensor)
            n = q_values.argmax().item()
            return (n % 5) + 1
            #return n

    def update(self):
        if len(self.replay_buffer) < self.batch_size:
            return None
        states, actions, rewards, next_states, dones = self.replay_buffer.sample(self.batch_size)
        states = torch.tensor(states, dtype=torch.float32).to(self.device)
        actions = torch.tensor(actions, dtype=torch.int64).unsqueeze(1).to(self.device)
        rewards = torch.tensor(rewards, dtype=torch.float32).unsqueeze(1).to(self.device)
        next_states = torch.tensor(next_states, dtype=torch.float32).to(self.device)
        dones = torch.tensor(dones, dtype=torch.float32).unsqueeze(1).to(self.device)

        q_values = self.q_network(states).gather(1, actions)
        with torch.no_grad():
            max_next_q_values = self.target_network(next_states).max(1)[0].unsqueeze(1)
            target = rewards + self.gamma * max_next_q_values * (1 - dones)
        loss = nn.MSELoss()(q_values, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def update_target(self):
        self.target_network.load_state_dict(self.q_network.state_dict())
