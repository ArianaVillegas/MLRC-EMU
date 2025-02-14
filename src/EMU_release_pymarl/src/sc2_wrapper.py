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
        # Aquí se puede aplicar el preprocesamiento que necesites:
        # Ejemplo: convertir imágenes a un vector plano
        return np.array(state).flatten()
