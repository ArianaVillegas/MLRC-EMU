class MultiAgentEnv(object):
    def __init__(self, **kwargs):
       
        from smac.env import StarCraft2Env  
       
        self.env = StarCraft2Env(**kwargs)
        self.env_info = self.env.get_env_info()
        self.n_agents = self.env_info.get("n_agents", None)
        self.episode_limit = self.env_info.get("episode_limit", None)
        self.unit_dim = self.env_info.get("unit_dim", None)

    def step(self, actions):
        """
        Takes a list of actions (one per agent) and returns (reward, terminated, info).
        """
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
        Sets the environment seed.
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
