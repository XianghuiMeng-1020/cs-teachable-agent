def summarize_observations():
    logs = {}
    try:
        with open('spaceship_logs.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    spaceship_name, planet_name, observation = line.split(':', 2)
                    unique_key = (planet_name, observation)
                    if spaceship_name not in logs:
                        logs[spaceship_name] = set()
                    logs[spaceship_name].add(unique_key)

        with open('summary.txt', 'w') as summary_file:
            for spaceship, unique_observations in logs.items():
                summary_file.write(f'{spaceship}:{len(unique_observations)}\n')
    except Exception:
        with open('summary.txt', 'w') as summary_file:
            summary_file.write('')