import numpy as np

class SC2Wrapper:
    def __init__(self, env):
        self.env = env

    def reset(self):
        state = self.env.reset()
        return self.preprocess(state)

    def step(self, action):
        next_state, reward, done, info = self.env.step(action)
        return self.preprocess(next_state), reward, done, info

    def preprocess(self, state):
        return np.array(state).flatten()
