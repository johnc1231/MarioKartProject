import retro
import copy
import time
import gzip
import os

GO = 0
BRAKE = 1
LEFT = 6
RIGHT = 7
BRAKE_2 = 9


def save_state(env, state_dir, statename, inttype=retro.data.Integrations.DEFAULT):
    if not statename.endswith('.state'):
        statename += '.state'

    state_bytes = env.em.get_state()
    gzipped_state = gzip.compress(state_bytes)
    file_name = os.path.join(state_dir, statename)

    with open(file_name, "wb+") as f:
        f.write(gzipped_state)

        

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
    for i in range(0, 3):
        env.load_state(statename)
        env.reset()
        act = actions[i]
        reward = 0
        for j in range(0, num_frames):
            obs, rew, done, info = env.step(act)
            time.sleep(.01)
            env.render()
            reward = rew
        rewards[i] = reward
        save_state(env, "states/search_generated", "{}.state".format(i))

    print(rewards)

    return actions[rewards.index(max(rewards))]


def main():
    env = retro.make(game="SuperMarioKart-Snes")
    obs = env.reset()
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
