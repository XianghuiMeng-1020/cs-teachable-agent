def summarize_observations():
    spaceship_observations = {}
    try:
        with open('spaceship_logs.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    spaceship_name, planet_name, observation = line.split(':')
                    if spaceship_name not in spaceship_observations:
                        spaceship_observations[spaceship_name] = {}
                    if planet_name not in spaceship_observations[spaceship_name]:
                        spaceship_observations[spaceship_name][planet_name] = set()
                    spaceship_observations[spaceship_name][planet_name].add(observation)
        with open('summary.txt', 'w') as f:
            for spaceship_name, planets in spaceship_observations.items():
                unique_observations_count = sum(len(observations) for observations in planets.values())
                f.write(f'{spaceship_name}:{unique_observations_count}\n')
    except Exception:
        with open('summary.txt', 'w') as f:
            f.write('')
