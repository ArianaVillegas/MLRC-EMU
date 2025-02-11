from ai2thor.controller import Controller
import numpy as np

class iTHOREnvWrapper:
    def __init__(self, config):
        self.controller = Controller(
            agentMode=config["agent_mode"],
            scene=config["scene"],
            gridSize=config["grid_size"],
            visibilityDistance=config["visibility_distance"],
            width=config["render_width"],
            height=config["render_height"]
        )
        
        self.actions = ["MoveAhead", "RotateLeft", "RotateRight", "LookUp", "LookDown", "Pickup", "Drop"]
        self.observation_space = self._get_obs_space()
        
    def _get_obs_space(self):
        return {
            'image': (3, 224, 224),
            'objects': list,
            'inventory': dict
        }
    
    def reset(self):
        self.controller.reset()
        return self._process_obs()
    
    def step(self, action):
        event = self.controller.step(action=self.actions[action])
        return self._process_obs(), self._get_reward(event), event.metadata["lastActionSuccess"], {}
    
    def _process_obs(self):
        return {
            'image': np.array(self.controller.last_event.frame),
            'objects': self.controller.last_event.metadata["objects"],
            'inventory': self.controller.last_event.metadata["inventory"]
        }
    
    def _get_reward(self, event):
        return 1.0 if event.metadata["lastActionSuccess"] else -0.1