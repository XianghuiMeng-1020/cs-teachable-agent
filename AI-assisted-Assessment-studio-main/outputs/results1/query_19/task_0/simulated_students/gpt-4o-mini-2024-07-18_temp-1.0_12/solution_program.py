def summarize_observations():
    from collections import defaultdict

    spaceship_observations = defaultdict(set)

    try:
        with open('spaceship_logs.txt', 'r') as log_file:
            for line in log_file:
                line = line.strip()
                if line:
                    spaceship_name, planet_name, observation = line.split(':')
                    unique_key = (planet_name, observation)
                    spaceship_observations[spaceship_name].add(unique_key)
    except Exception:
        with open('summary.txt', 'w') as summary_file:
            pass
        return

    with open('summary.txt', 'w') as summary_file:
        for spaceship_name, unique_obs in spaceship_observations.items():
            summary_file.write(f'{spaceship_name}:{len(unique_obs)}\n')