def summarize_observations():
    import os
    from collections import defaultdict

    logs_file = 'spaceship_logs.txt'
    summary_file = 'summary.txt'

    # Dictionary to hold unique observations for each spaceship
    spaceship_observations = defaultdict(set)

    try:
        with open(logs_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                spaceship_name, planet_name, observation = line.split(':')
                # Use a set to store unique observations per spaceship and planet
                spaceship_observations[spaceship_name].add((planet_name, observation))

    except (FileNotFoundError, ValueError):
        # Handle errors by creating an empty summary file
        with open(summary_file, 'w') as summary:
            pass  # Empty file
        return

    # Write the summary to the summary.txt file
    with open(summary_file, 'w') as summary:
        for spaceship_name, observations in spaceship_observations.items():
            summary.write(f'{spaceship_name}:{len(observations)}\n')