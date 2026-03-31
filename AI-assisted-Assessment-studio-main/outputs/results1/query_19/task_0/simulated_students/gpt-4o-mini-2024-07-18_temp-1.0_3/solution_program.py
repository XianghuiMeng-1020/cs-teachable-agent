def summarize_observations():
    from collections import defaultdict

    # Dictionary to hold unique observations per spaceship
    observations = defaultdict(set)

    try:
        # Read the spaceship_logs.txt file
        with open('spaceship_logs.txt', 'r') as log_file:
            for line in log_file:
                # Split each line into components
                parts = line.strip().split(':')
                if len(parts) == 3:
                    spaceship_name, planet_name, observation = parts
                    # Use a set to track unique observations for each spaceship
                    observations[spaceship_name].add((planet_name, observation))
    except Exception as e:
        # In case of any error, create an empty summary.txt file
        with open('summary.txt', 'w') as summary_file:
            summary_file.write('')
        return

    # Write the summary to summary.txt file
    with open('summary.txt', 'w') as summary_file:
        for spaceship, obs_set in observations.items():
            # Count unique observations by size of set
            summary_file.write(f'{spaceship}:{len(obs_set)}\n')
