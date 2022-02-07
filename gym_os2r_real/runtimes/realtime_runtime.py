from gym_ignition.base import runtime, task
from gym_ignition.utils.typing import Action, Done, Info, Observation, State
from gym_ignition.utils import logger

from scenario import monopod as scenario
import real_time_tools as rt

import numpy as np


class RealTimeRuntime(runtime.Runtime):
    """
    Implementation of :py:class:`~gym_ignition.base.runtime.Runtime` for
    real-time execution.

    Warning:
        This class is not yet complete.
    """

    def __init__(self, task_cls: type, agent_rate: float, task_mode: str,
                 **kwargs):

        self.task_mode = task_mode
        # World attributes
        self._world = None
        self._model = None

        # Build the environment
        task_object = task_cls(agent_rate=agent_rate, task_mode=task_mode,
         **kwargs)

        assert isinstance(
            task_object, task.Task
        ), "'task_cls' object must inherit from Task"

        super().__init__(task=task_object, agent_rate=agent_rate)

        # Initialize the scenario world through property decorator
        _ = self.world
        _ = self.model

        # Initialize the spaces
        self.action_space, self.observation_space = self.task.create_spaces()

        # Store the spaces also in the task
        self.task.action_space = self.action_space
        self.task.observation_space = self.observation_space

        self.spinner = rt.FrequencyManager(agent_rate)  # real time spinner.

    # =================
    # Runtime interface
    # =================

    def timestamp(self) -> float:

        raise NotImplementedError

    # =================
    # gym.Env interface
    # =================

    def step(self, action: Action) -> State:

        # Validate action and robot
        assert self.action_space.contains(action), "%r (%s) invalid" % (
            action,
            type(action),
        )

        # Set the action
        ok_action = self.task.set_action(action)
        assert ok_action, "Failed to set the action"

        # TODO: check real time loop speed to make sure it is possible.
        if not self.spinner.wait():
            logger.warn("Realtime_Runtime missed Realtime controller rate. "
            "Make sure that the agent_rate is suitable for realtime guarntee.")

        # Get the observation
        observation = self.task.get_observation()
        assert self.observation_space.contains(observation), "%r (%s) invalid" % (
            observation,
            type(observation),
        )

        # Get the reward
        reward = self.task.get_reward()

        # Check termination
        done = self.task.is_done()

        return State((observation, reward, Done(done), Info({})))

    def reset(self) -> Observation:

        # Reset the task
        self.task.reset_task()

        # # # TODO: add pause (for manual reset)
        # # Wait for external input before continuing.
        # input("Press Enter when robot is in its reset position...")

        # Get the observation
        observation = self.task.get_observation()
        assert isinstance(observation, np.ndarray)

        if not self.observation_space.contains(observation):
            logger.warn(
                "The observation does not belong to the observation space")

        # Spin here to avoid warning in step.
        self.spinner.wait()

        return Observation(observation)

    def render(self, mode: str = "human", **kwargs) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    @property
    def world(self) -> scenario.World:

        if self._world is not None:
            # assert self._world.valid()
            return self._world

        # Create the world
        world = scenario.World()
        modes = {
        "free_hip" : scenario.Mode_free,
        "fixed_hip" : scenario.Mode_fixed_connector,
        "fixed" : scenario.Mode_fixed
        }

        # TODO: Remove the dummy mode
        world.initialize(modes[self.task_mode], True)
        # world.initialize(modes[self.task_mode])

        # Set the world in the task
        self.task.world = world

        # Store the world in runtime
        self._world = world

        return self._world

    @property
    def model(self) -> scenario.Model:

        if self._model is not None:
            return self._model

        # Create the model
        model_name = self._world.model_names()[0]
        model = self._world.get_model(model_name)

        # Set the model in the task
        self.task.model = model
        assert model.valid(), "Model is not valid."

        # Set the model name in the task.
        self.task.model_name = model.name()

        # TODO: Set joint limits here.

        # for joint in self._model.joints():
        #     name = joint.name()
        #
        #     joint.set_joint_position_limit(max, min)
        #     joint.set_joint_velocity_limit(max, min)

        # Store the model in runtime

        self._model = model

        return self._model
