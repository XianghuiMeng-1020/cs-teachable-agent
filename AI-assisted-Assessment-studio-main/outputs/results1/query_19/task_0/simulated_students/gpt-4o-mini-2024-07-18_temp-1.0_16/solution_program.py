def summarize_observations():
    logs = {}
    try:
        with open('spaceship_logs.txt', 'r') as file:
            for line in file:
                spaceship, planet, observation = line.strip().split(':')
                if spaceship not in logs:
                    logs[spaceship] = set()
                logs[spaceship].add((planet, observation))
    except FileNotFoundError:
        open('summary.txt', 'w').close()  # Create empty summary file if logs file not found
        return  # Exit the function if there is an error

    with open('summary.txt', 'w') as summary_file:
        for spaceship, observations in logs.items():
            unique_observations_count = len(observations)
            summary_file.write(f'{spaceship}:{unique_observations_count}\n')
