import retro
import copy
import time
import gzip
import os
from util import *

GO = 0
BRAKE = 1
LEFT = 6
RIGHT = 7
BRAKE_2 = 9

        

def generate_action(index_list):
    action = [0] * 12
    for index in index_list:
        action[index] = 1
    return action

left_action = generate_action([GO, LEFT])
right_action = generate_action([GO, RIGHT])
straight_action = generate_action([GO])

#maybe dump all of data
def select_best_action(env, statename, num_frames):
    actions = [left_action, right_action, straight_action]
    rewards = [None, None, None]
    finished = False
    for i in range(0, 3):
        load_state(env, statename)
        env.reset()
        act = actions[i]
        reward = 0
        for j in range(0, num_frames):
            obs, rew, done, info = env.step(act)
            finished = done or finished
            time.sleep(.01)
            env.render()
            reward = rew
        rewards[i] = reward
        save_state(env, "states/search_generated", "{}.state".format(i))

    best_index = rewards.index(max(rewards))

    return (actions[best_index], "states/search_generated/{}.state".format(best_index), finished)


def main():
    env = retro.make(game="SuperMarioKart-Snes")
    obs = env.reset()
    state = "states/Mario-Circuit-Start.state"
    done = False
    while (not done):
        action, state, done = select_best_action(env, state, 20)
        print(action)

    #oldEnv = copy.deepcopy(env)
    # frame_count = 0
    # while True:
    #     action = straight_action
    #     action[GO] = 1
    #     action[BRAKE] = 0
    #     action[BRAKE_2] = 0
    #     obs, rew, done, info = env.step(action)
    #     env.render()
    #     print(rew)
    #     frame_count += 1
    #     if frame_count >= 100:
    #         frame_count = 0
    #         env.reset()
    #     # if done:
    #     #     obs = env.reset()
    # env.close()
    print(select_best_action(env, "Mario-Circuit-Start.state", 100))
    env.close()


if __name__ == "__main__":
    main()
