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

def angle_to_action_sequence(angle, max_angle, num_frames):
    default = None
    if angle < 0:
        default = left_action
    else: 
        default = right_action
    how_often_straight = int((max_angle - abs(angle)))
    return [straight_action if (how_often_straight == 0 or i % how_often_straight == 0) else default for i in range(0, num_frames)]
        

#maybe dump all of data
def select_best_action(env, statename, num_frames):
    max_angle = 10
    actions = [left_action, straight_action, right_action]
    rewards = [None] * (max_angle * 2 + 1)
    finished = False
    for i in range(-max_angle, max_angle):
        load_state(env, statename)
        env.reset()
        # act = actions[i]
        reward = 0
        actions = angle_to_action_sequence(i, max_angle, num_frames)
        print(i)
        for counter, act in enumerate(actions):
        # for j in range(0, num_frames):
            obs, rew, done, info = env.step(act)
            finished = done or finished
            time.sleep(.01)
            env.render()
            reward = rew
        rewards[i + max_angle] = reward
        save_state(env, "states/search_generated", "{}.state".format(i))

    print(rewards)
    best_index = rewards.index(max(rewards))
    best_angle = best_index + max_angle
    print("GOING {}".format(best_angle))
    time.sleep(1)

    return (actions[best_index], "states/search_generated/{}.state".format(best_angle), finished)


def main():
    env = retro.make(game="SuperMarioKart-Snes")
    obs = env.reset()
    state = "states/Mario-Circuit-Start.state"
    done = False
    while (not done):
        action, state, done = select_best_action(env, state, 200)
        print("Loading state: {}".format(state))

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
