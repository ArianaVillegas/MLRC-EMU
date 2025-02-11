import torch
import torch.nn as nn
import numpy as np
from components.episodic_memory_buffer import EpisodicMemoryBuffer

class DQNAgent(nn.Module):
    def __init__(self, args):
        super().__init__()
        self.args = args
        
        # Red Q
        self.q_net = nn.Sequential(
            nn.Conv2d(3, 32, 8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, 4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, stride=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(3136 + args.emdqn_latent_dim, 512),
            nn.ReLU(),
            nn.Linear(512, args.n_actions)
        )
        
        # Memoria Episódica
        self.memory = EpisodicMemoryBuffer(args, scheme={
            'state': {'vshape': 3136},  
            'actions': {'vshape': 1},
            'reward': {'vshape': 1}
        })
        
        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=args.lr)
    
    def act(self, obs):
        if np.random.random() < self.args.epsilon:
            return np.random.randint(len(self.args.actions))
        
        with torch.no_grad():
            state_tensor = torch.tensor(obs['image']).permute(2,0,1).unsqueeze(0).float()
            memory_context = self.memory.retrieve(state_tensor)
            q_values = self.q_net(torch.cat([state_tensor, memory_context], dim=1))
            return torch.argmax(q_values).item()