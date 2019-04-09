import retro
import copy
import time
import gzip
import os
from PIL import Image
import numpy as np
from datetime import datetime
from keras.models import load_model

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

def keras_output_to_action(keras_output):
    if keras_output[0]:
        return left_action
    elif keras_output[1]:
        return straight_action
    else:
        return right_action

left_action = generate_action([GO, LEFT])
right_action = generate_action([GO, RIGHT])
straight_action = generate_action([GO])

def main():
    env = retro.make(game="SuperMarioKart-Snes")
    obs = env.reset()
    state = "Mario-Circuit3.state"
    env.load_state(state)
    env.reset()
    done = False
    frame_count = 0

    model = load_model("model_1.hd5")
    action = straight_action
    while (not done):
        obs, rew, done, info = env.step(action)
        img = Image.fromarray(obs, 'RGB').convert("L")
        img = img.crop((0, 0, img.width, img.height/2))
        #x_scaled_numpy = np.array([np.array(im).reshape((im.height, im.width, 1)) * (1.0 / 256.0) for im in x_images])
        np_img = np.array(img).reshape((img.height, img.width, 1)) * (1.0 / 256.0)
        predicted = np.around(model.predict(np.array([np_img])))[0]
        print(predicted)
        action = keras_output_to_action(predicted)
        print(action)
        env.render()
        frame_count += 1
    env.close()


if __name__ == "__main__":
    main()
