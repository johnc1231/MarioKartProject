import os
import gzip 
import retro

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