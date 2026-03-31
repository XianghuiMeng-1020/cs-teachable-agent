def summarize_observations():
    observations = {}
    try:
        with open('spaceship_logs.txt', 'r') as file:
            for line in file:
                # Split the line into components
                spaceship, planet, observation = line.strip().split(':')
                # Create a unique key for each spaceship and planet
                key = (spaceship, planet)
                # Use a set to store unique observations for each (spaceship, planet) pair
                if key not in observations:
                    observations[key] = set()
                # Add the observation to the respective set
                observations[key].add(observation)

        summary = {}
        # Count unique observations for each spaceship
        for (spaceship, planet), obs_set in observations.items():
            if spaceship not in summary:
                summary[spaceship] = 0
            summary[spaceship] += len(obs_set)

        # Write the summary to summary.txt
        with open('summary.txt', 'w') as summary_file:
            for spaceship, unique_count in summary.items():
                summary_file.write(f'{spaceship}:{unique_count}\n')
    except Exception:
        # In case of an error, create an empty summary.txt
        with open('summary.txt', 'w') as summary_file:
            pass