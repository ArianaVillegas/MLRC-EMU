# Archivo: src/EMU_release_pymarl/src/envs/multiagentenv.py

from smac.env import StarCraft2Env

class MultiAgentEnv:
    def __init__(self, **kwargs):
       
        self.env = StarCraft2Env(**kwargs)
        self.env_info = self.env.get_env_info()
    
    def get_obs_size(self):
       
        return self.env_info["obs_size"]
    
    def get_total_actions(self):
      
        return self.env_info["n_actions"]
    
    def reset(self):
        return self.env.reset()
    
    def step(self, actions):
        return self.env.step(actions)
