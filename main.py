import retro
from matplotlib import pyplot as plt
import copy

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

def select_best_action():
    return None

def main():
    env = retro.make(game="SuperMarioKart-Snes")
    print(dir(env))
    obs = env.reset()
    oldEnv = copy.deepcopy(env)
    frame_count = 0
    while True:
        action = straight_action
        action[GO] = 1
        action[BRAKE] = 0
        action[BRAKE_2] = 0
        obs, rew, done, info = env.step(action)
        env.render()
        print(rew)
        frame_count += 1
        if frame_count >= 100:
            frame_count = 0
            env = oldEnv
        # if done:
        #     obs = env.reset()
    env.close()


if __name__ == "__main__":
    main()
