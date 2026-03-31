def summarize_observations():
    spaceship_observations = {}
    try:
        with open('spaceship_logs.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                spaceship_name, planet_name, observation = line.split(':')
                if spaceship_name not in spaceship_observations:
                    spaceship_observations[spaceship_name] = set()
                # Create a unique key for observation based on spaceship and planet
                unique_key = (planet_name, observation)
                spaceship_observations[spaceship_name].add(unique_key)

        with open('summary.txt', 'w') as summary_file:
            for spaceship_name, observations in spaceship_observations.items():
                summary_file.write(f'{spaceship_name}:{len(observations)}\n')
    except Exception:
        with open('summary.txt', 'w') as summary_file:
            summary_file.write('')