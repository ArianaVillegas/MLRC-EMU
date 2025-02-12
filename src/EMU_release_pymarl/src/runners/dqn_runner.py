from envs import REGISTRY as env_REGISTRY
from functools import partial
from components.episode_buffer import EpisodeBatch
from multiprocessing import Pipe, Process
import numpy as np
import torch as th

class DQNRunner:
    def __init__(self, args, logger):
        self.args = args
        self.logger = logger
        self.batch_size = self.args.batch_size_run

     
        self.parent_conns, self.worker_conns = zip(*[Pipe() for _ in range(self.batch_size)])
        env_fn = env_REGISTRY[self.args.env]
        self.ps = [Process(target=env_worker, args=(worker_conn, CloudpickleWrapper(partial(env_fn, **self.args.env_args))))
                   for worker_conn in self.worker_conns]

        for p in self.ps:
            p.daemon = True
            p.start()

        self.parent_conns[0].send(("get_env_info", None))
        self.env_info = self.parent_conns[0].recv()
        self.episode_limit = self.env_info["episode_limit"]

        self.t = 0
        self.t_env = 0

        self.train_returns = []
        self.test_returns = []
        self.train_stats = {}
        self.test_stats = {}

        self.log_train_stats_t = -100000

    def setup(self, scheme, groups, preprocess, mac):
        self.new_batch = partial(EpisodeBatch, scheme, groups, self.batch_size, self.episode_limit + 1,
                                 preprocess=preprocess, device=self.args.device)
        self.mac = mac
        self.scheme = scheme
        self.groups = groups
        self.preprocess = preprocess

    def run(self, test_mode=False):
        self.batch = self.new_batch()
        self._reset_envs()
        
        episode_returns = [0 for _ in range(self.batch_size)]
        terminated = [False for _ in range(self.batch_size)]
        envs_not_terminated = [b_idx for b_idx, termed in enumerate(terminated) if not termed]

        while not all(terminated):
            actions = self.mac.select_actions(self.batch, t_ep=self.t, t_env=self.t_env, bs=envs_not_terminated, test_mode=test_mode)
            cpu_actions = actions.to("cpu").numpy()
            self._step_envs(cpu_actions, envs_not_terminated, episode_returns, terminated)
            envs_not_terminated = [b_idx for b_idx, termed in enumerate(terminated) if not termed]
            self.t += 1

        if not test_mode:
            self.t_env += sum(episode_returns)

        return self.batch

    def _reset_envs(self):
        for parent_conn in self.parent_conns:
            parent_conn.send(("reset", None))

        pre_transition_data = {"state": [], "avail_actions": [], "obs": []}
        for parent_conn in self.parent_conns:
            data = parent_conn.recv()
            pre_transition_data["state"].append(data["state"])
            pre_transition_data["avail_actions"].append(data["avail_actions"])
            pre_transition_data["obs"].append(data["obs"])
        
        self.batch.update(pre_transition_data, ts=0)
        self.t = 0

    def _step_envs(self, cpu_actions, envs_not_terminated, episode_returns, terminated):
        for idx, parent_conn in enumerate(self.parent_conns):
            if idx in envs_not_terminated:
                parent_conn.send(("step", cpu_actions[idx]))
        
        post_transition_data = {"reward": [], "terminated": []}
        pre_transition_data = {"state": [], "avail_actions": [], "obs": []}
        
        for idx, parent_conn in enumerate(self.parent_conns):
            if not terminated[idx]:
                data = parent_conn.recv()
                post_transition_data["reward"].append((data["reward"],))
                terminated[idx] = data["terminated"]
                episode_returns[idx] += data["reward"]
                pre_transition_data["state"].append(data["state"])
                pre_transition_data["avail_actions"].append(data["avail_actions"])
                pre_transition_data["obs"].append(data["obs"])
        
        self.batch.update(post_transition_data, bs=envs_not_terminated, ts=self.t, mark_filled=False)
        self.batch.update(pre_transition_data, bs=envs_not_terminated, ts=self.t + 1, mark_filled=True)


def env_worker(remote, env_fn):
    env = env_fn.x()
    while True:
        cmd, data = remote.recv()
        if cmd == "step":
            reward, terminated, env_info = env.step(data)
            remote.send({
                "state": env.get_state(),
                "avail_actions": env.get_avail_actions(),
                "obs": env.get_obs(),
                "reward": reward,
                "terminated": terminated,
                "info": env_info
            })
        elif cmd == "reset":
            env.reset()
            remote.send({
                "state": env.get_state(),
                "avail_actions": env.get_avail_actions(),
                "obs": env.get_obs()
            })
        elif cmd == "close":
            env.close()
            remote.close()
            break
        elif cmd == "get_env_info":
            remote.send(env.get_env_info())
        else:
            raise NotImplementedError

class CloudpickleWrapper():
    def __init__(self, x):
        self.x = x
    def __getstate__(self):
        import cloudpickle
        return cloudpickle.dumps(self.x)
    def __setstate__(self, ob):
        import pickle
        self.x = pickle.loads(ob)
