import torch
import random

class DQNRunner:
    def __init__(self, config, env, agent, logger):
        self.config = config
        self.env = env
        self.agent = agent
        self.logger = logger
        self.max_episodes = config.get("max_episodes", 500)
        self.epsilon = config.get("epsilon_start", 1.0)
        self.epsilon_decay = config.get("epsilon_decay", 0.995)
        self.epsilon_min = config.get("epsilon_min", 0.1)
        self.target_update_freq = config.get("target_update_freq", 1000)
        self.total_steps = 0

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
