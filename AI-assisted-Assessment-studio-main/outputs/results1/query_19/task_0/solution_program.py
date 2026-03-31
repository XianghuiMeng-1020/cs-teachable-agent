def summarize_observations():
    try:
        with open('spaceship_logs.txt', 'r') as f:
            logs = f.readlines()
    except IOError:
        with open('summary.txt', 'w') as sf:
            sf.write('')
        return

    observations = {}
    for log in logs:
        parts = log.strip().split(':')
        if len(parts) != 3:
            continue
        spaceship, planet, observation = parts
        key = (spaceship, planet)
        if key not in observations:
            observations[key] = set()
        observations[key].add(observation)

    summary = {}
    for (spaceship, _), unique_obs in observations.items():
        if spaceship not in summary:
            summary[spaceship] = 0
        summary[spaceship] += len(unique_obs)

    with open('summary.txt', 'w') as sf:
        for spaceship, count in summary.items():
            sf.write(f'{spaceship}:{count}\n')