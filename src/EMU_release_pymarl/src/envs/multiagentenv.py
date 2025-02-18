##from smac.env import StarCraft2Env
import smac.env.starcraft2.starcraft2_EMU as starcraft
#nano MLRC-EMU/src/EMU_release_pymarl/src/envs/multiagentenv.py

class MultiAgentEnv(object):
    def __init__(self, **kwargs):
    
        self.env = starcraft.StarCraft2Env(**kwargs)
        try:
            self.env_info = self.env.get_env_info()
        except AttributeError:
        
            try:
                obs_size = self.env.get_obs_size()
            except AttributeError:
                obs_size = None
            try:
                state_size = self.env.get_state_size()
            except AttributeError:
                state_size = None
            try:
                n_actions = self.env.get_total_actions()
            except AttributeError:
                n_actions = None

            n_agents = getattr(self.env, "n_agents", None)
            episode_limit = getattr(self.env, "episode_limit", None)
            unit_dim = getattr(self.env, "unit_dim", None)

            self.env_info = {
                "obs_shape": obs_size,
                "state_shape": state_size,
                "n_actions": n_actions,
                "n_agents": n_agents,
                "episode_limit": episode_limit,
                "unit_dim": unit_dim
            }

        self.n_agents = self.env_info.get("n_agents", None)
        self.episode_limit = self.env_info.get("episode_limit", None)
        self.unit_dim = self.env_info.get("unit_dim", None)

    def step(self, actions):
        """
        Takes a list of actions (one per agent) and returns (reward, terminated, info).
        """
        print("actions", actions)
        ## transforma a array porque arroja solo 1
        if isinstance(actions, int):
            actions = [actions]
        reward, terminated, info = self.env.step(actions)
        return reward, terminated, info

    def get_obs(self):
        """
        Returns the list of observations for each agent.
        """
        return self.env.get_obs()

    def get_obs_agent(self, agent_id):
        """
        Returns the observation for the specified agent.
        """
        return self.env.get_obs_agent(agent_id)

    def get_obs_size(self):
        """
        Returns the observation size as defined in SMAC.
        """
        return self.env_info["obs_shape"]

    def get_state(self):
        """
        Returns the global state.
        """
        return self.env.get_state()

    def get_state_size(self):
        """
        Returns the global state size as defined in SMAC.
        """
        return self.env_info["state_shape"]

    def get_avail_actions(self):
        """
        Returns the available actions for all agents.
        """
        return self.env.get_avail_actions()

    def get_avail_agent_actions(self, agent_id):
        """
        Returns the available actions for the specified agent.
        """
        return self.env.get_avail_agent_actions(agent_id)

    def get_total_actions(self):
        """
        Returns the total number of actions an agent can take.
        """
        return self.env_info["n_actions"]

    def reset(self):
        """
        Resets the environment and returns the initial observations.
        """
        return self.env.reset()

    def render(self):
        """
        Renders the environment.
        """
        self.env.render()

    def close(self):
        """
        Closes the environment.
        """
        self.env.close()

    def seed(self, seed):
        """
        Sets the random seed for the environment.
        """
        self.env.seed(seed)

    def save_replay(self):
        """
        Saves the replay of the episode.
        """
        self.env.save_replay()

    def get_env_info(self):
        """
        Returns the environment information.
        """
        return self.env_info
