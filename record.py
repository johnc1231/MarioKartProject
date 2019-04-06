import retro
import copy
import time
import gzip
import os
import keyboard
from PIL import Image
import numpy as np
from datetime import datetime

# w, h = 512, 512
# data = np.zeros((h, w, 3), dtype=np.uint8)
# data[256, 256] = [255, 0, 0]
# img = Image.fromarray(data, 'RGB')
# img.save('my.png')
# img.show()

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

def main():
    env = retro.make(game="SuperMarioKart-Snes")
    obs = env.reset()
    state = "states/Mario-Circuit-Start.state"
    done = False
    frame_count = 0

    root_dir = os.getcwd()
    recording_dir = os.path.join(root_dir, "recorded_data/human_play")
    timestamp_string = str(datetime.now()).replace(" ", "-")
    data_folder_path = os.path.join(recording_dir, timestamp_string)
    os.makedirs(data_folder_path)
    image_folder_path = os.path.join(data_folder_path, "images")
    os.makedirs(image_folder_path)
    action_folder_path = os.path.join(data_folder_path, "actions")
    os.makedirs(action_folder_path)
    while (not done):
        action = straight_action
        if (keyboard.is_pressed("left")):
            action = left_action
        elif (keyboard.is_pressed("right")):
            action = right_action
        elif (keyboard.is_pressed("q")):
            break
        
        time.sleep(.01)
 
        obs, rew, done, info = env.step(action)
        env.render()
        if frame_count % 10 == 0:
            img = Image.fromarray(obs, 'RGB')
            image_path = os.path.join(image_folder_path, "frame_{}.png".format(frame_count))
            img.save(image_path)
            os.chmod(image_path, 0o777)
            action_path = os.path.join(action_folder_path, "frame_{}.csv".format(frame_count))
            np.savetxt(action_path, action, delimiter=",", fmt="%d")
        frame_count += 1
    env.close()


if __name__ == "__main__":
    main()
