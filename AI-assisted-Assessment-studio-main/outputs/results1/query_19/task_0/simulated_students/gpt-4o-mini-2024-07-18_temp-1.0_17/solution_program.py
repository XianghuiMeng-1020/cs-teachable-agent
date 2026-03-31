def summarize_observations():
    from collections import defaultdict

    logs = defaultdict(set)

    try:
        with open('spaceship_logs.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    spaceship_name, planet_name, observation = line.split(':', 2)
                    logs[spaceship_name].add((planet_name, observation))
    except Exception:
        open('summary.txt', 'w').close()  # Create an empty summary file
        return

    with open('summary.txt', 'w') as summary_file:
        for spaceship_name, observations in logs.items():
            summary_file.write(f'{spaceship_name}:{len(observations)}\n')