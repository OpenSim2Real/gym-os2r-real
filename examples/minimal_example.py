import gym
import time
import gym_os2r_real
from gym_ignition.utils import logger


# Set verbosity
# logger.set_level(gym.logger.ERROR)
# logger.set_level(gym.logger.WARN)
logger.set_level(gym.logger.DEBUG)

# Available tasks
env_id = "Real-monopod-simple-v1"

env = gym.make(env_id)
for epoch in range(2):

    # Reset the environment
    observation = env.reset()

    # Initialize returned values
    done = False
    count = 0
    while not done:
        action = env.action_space.sample() * 0.1
        observation, reward, done, _ = env.step(action)
        count += 1
        if (count % env.agent_rate == 0):
            print("Second.", count/env.agent_rate)

env.close()
time.sleep(5)
