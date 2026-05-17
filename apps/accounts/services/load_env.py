def load_env(path):
    env = {}

    with open(path) as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            key, value = line.split("=", 1)

            env[key.strip()] = value.strip()

    return env
