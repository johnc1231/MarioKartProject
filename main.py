import retro

A = 0
BRAKE = 1
LEFT = 6
RIGHT = 7
BRAKE_2 = 9



def main():
    env = retro.make(game="SuperMarioKart-Snes")
    obs = env.reset()
    print(env.action_space.sample())
    while True:
        # action = env.action_space.sample()
        action = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        obs, rew, done, info = env.step(action)
        env.render()
        if done:
            obs = env.reset()
    env.close()


if __name__ == "__main__":
    main()
