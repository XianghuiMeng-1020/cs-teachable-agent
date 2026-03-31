def summarize_observations():
    import os

    # Initialize a dictionary to hold observations
    observations = {}

    try:
        with open('spaceship_logs.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) != 3:
                    continue
                spaceship_name, planet_name, observation = parts

                # Initialize a set for each spaceship and planet combination
                if spaceship_name not in observations:
                    observations[spaceship_name] = {}
                if planet_name not in observations[spaceship_name]:
                    observations[spaceship_name][planet_name] = set()

                # Add the observation to the set (unique per planet)
                observations[spaceship_name][planet_name].add(observation)

        # Preparing output for summary.txt
        summary_lines = []
        for spaceship_name, planets in observations.items():
            unique_observations_count = sum(len(obs) for obs in planets.values())
            summary_lines.append(f'{spaceship_name}:{unique_observations_count}') 

        with open('summary.txt', 'w') as summary_file:
            for line in summary_lines:
                summary_file.write(line + '\n')
    except Exception:
        with open('summary.txt', 'w') as summary_file:
            summary_file.write('')