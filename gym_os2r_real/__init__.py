import numpy
from . import runtimes
from gym_os2r import tasks

__all__ = ['runtimes']

from gym.envs.registration import register
from gym_os2r.rewards import StandingV3
# from gym_os2r.rewards import BalancingV1, StandingV1, StandingV2, StandingV3, WalkingV1

register(
    id = 'Real-monopod-stand-v1',
    entry_point = 'gym_os2r_real.runtimes.realtime_runtime:RealTimeRuntime',
    max_episode_steps = 100000,
    kwargs={'task_cls': tasks.monopod.MonopodTask,
            'agent_rate': 1000,
            'task_mode': 'free_hip',
            'reward_class': StandingV3,
            'reset_positions': ['ground']
            })