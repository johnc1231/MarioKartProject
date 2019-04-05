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

def load_state(env, statename, inttype=retro.data.Integrations.DEFAULT):
        if not statename.endswith('.state'):
                statename += '.state'

        with gzip.open(statename) as fh:
            env.initial_state = fh.read()

        env.statename = statename
        

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
    actions = [left_action, straight_action, right_action]
    num_actions = len(actions)
    num_iterations = 5
    total_num = num_iterations * 2 + 1
    middle_action = total_num / 2
    rewards = [None] * total_num
    finished = False
    for i in range(0, total_num):
        load_state(env, statename)
        env.reset()
        act = left_action
        if (i == middle_action):
            act = straight_action
        elif i > middle_action:
            act = right_action
        mod = i % middle_action + 1
        for j in range(0, num_frames):
            act_to_take = act
            if (j % mod == 0):
                act_to_take = straight_action
            obs, rew, done, info = env.step(act_to_take)
            finished = done or finished
            reward = rew
        rewards[i] = reward
        save_state(env, "states/search_generated", "{}.state".format(i))

    best_index = rewards.index(max(rewards))

    return (best_index, "states/search_generated/{}.state".format(best_index), finished)


def main():
    env = retro.make(game="SuperMarioKart-Snes")
    obs = env.reset()
    state = "states/Mario-Circuit-Start.state"
    done = False
    while (not done):
        action, state, done = select_best_action(env, state, 100)
        load_state(env, state)
        env.render()
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
    print("FINISHED")


if __name__ == "__main__":
    main()
