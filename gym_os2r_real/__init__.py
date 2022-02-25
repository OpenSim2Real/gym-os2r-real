import numpy
from . import runtimes
from gym_os2r import tasks

__all__ = ['runtimes']

from gym.envs.registration import register
<<<<<<< HEAD
from gym_os2r.rewards import StraightV1, HoppingV1, BalancingV2
=======
from gym_os2r.rewards import StraightV1, HoppingV1
>>>>>>> 15571115d3dfd298734a03db5034c6477b828563
# from gym_os2r.rewards import BalancingV1, StandingV1, StandingV2, StandingV3, WalkingV1

register(
    id = 'Real-monopod-simple-v1',
    entry_point = 'gym_os2r_real.runtimes.realtime_runtime:RealTimeRuntime',
    max_episode_steps = 100000,
    kwargs={'task_cls': tasks.monopod.MonopodTask,
            'agent_rate': 1000,
            'task_mode': 'simple',
            'reward_class': StraightV1,
            'reset_positions': ['real']
            })


register(
    id = 'Real-monopod-hop-v1',
    entry_point = 'gym_os2r_real.runtimes.realtime_runtime:RealTimeRuntime',
    max_episode_steps = 100000,
    kwargs={'task_cls': tasks.monopod.MonopodTask,
            'agent_rate': 1000,
            'task_mode': 'fixed_hip',
            'reward_class': HoppingV1,
            'reset_positions': ['real']
            })
<<<<<<< HEAD


register(
    id = 'Real-monopod-balance-v1',
    entry_point = 'gym_os2r_real.runtimes.realtime_runtime:RealTimeRuntime',
    max_episode_steps = 100000,
    kwargs={'task_cls': tasks.monopod.MonopodTask,
            'agent_rate': 1000,
            'task_mode': 'fixed_hip',
            'reward_class': BalancingV2,
            'reset_positions': ['real']
            })
=======
>>>>>>> 15571115d3dfd298734a03db5034c6477b828563
