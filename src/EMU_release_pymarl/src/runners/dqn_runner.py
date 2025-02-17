import random
import torch
##nano MLRC-EMU/src/EMU_release_pymarl/src/runners/dqn_runner.py
class DQNRunner:
    def __init__(self, args, logger):
        self.args = args
        self.logger = logger

        ##print("args", self.args)
       
        from envs.multiagentenv import MultiAgentEnv
        self.env = MultiAgentEnv()
        
      
        obs_dim = self.env.get_obs_size()
        action_dim = self.env.get_total_actions()
        
      
        from modules.agents.dqn_agent import DQNAgent
        self.agent = DQNAgent(obs_dim, action_dim, args.agent_args)
        
    

        '''     
        self.max_episodes = args.get("max_episodes", 500)
        self.epsilon = args.get("epsilon_start", 1.0)
        self.epsilon_decay = args.get("epsilon_decay", 0.995)
        self.epsilon_min = args.get("epsilon_min", 0.1)
        self.target_update_freq = args.get("target_update_freq", 1000)
        self.total_steps = 0
        '''
    	self.max_episodes = getattr(args, "max_episodes", 500)
        self.epsilon = getattr(args, "epsilon_start", 1.0)
        self.epsilon_decay = getattr(args, "epsilon_decay", 0.995)
        self.epsilon_min = getattr(args, "epsilon_min", 0.1)
        self.target_update_freq = getattr(args, "target_update_freq", 1000)
        self.total_steps = 0


        print("self.max_episodes", self.max_episodes)
        print("self.epsilon", self.epsilon)
        print("self.epsilon_decay", self.epsilon_decay)
        print("self.epsilon_min", self.epsilon_min)
        print("self.target_update_freq", self.target_update_freq)
        print("self.total_steps", self.total_steps)

    def run(self):
        for episode in range(self.max_episodes):
            state = self.env.reset()
            done = False
            episode_reward = 0
            while not done:
                action = self.agent.act(state, self.epsilon)
                next_state, reward, done, info = self.env.step(action)
                self.agent.replay_buffer.push(state, action, reward, next_state, done)
                state = next_state
                episode_reward += reward
                self.total_steps += 1

                loss = self.agent.update()
                if self.total_steps % self.target_update_freq == 0:
                    self.agent.update_target()
            self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
            self.logger.info(f"Episode {episode}: Reward {episode_reward:.2f} | Epsilon {self.epsilon:.3f}")

    def get_env_info(self):
        return self.env.get_env_info()