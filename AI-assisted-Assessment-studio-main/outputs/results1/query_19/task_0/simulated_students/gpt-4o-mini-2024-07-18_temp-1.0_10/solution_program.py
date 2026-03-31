def summarize_observations():
    summary = {}
    try:
        with open('spaceship_logs.txt', 'r') as file:
            for line in file:
                if line.strip():
                    spaceship_name, planet_name, observation = line.strip().split(':')
                    key = (spaceship_name, planet_name)
                    if key not in summary:
                        summary[key] = set()
                    summary[key].add(observation)
        output = {}
        for (spaceship_name, planet_name), observations in summary.items():
            if spaceship_name not in output:
                output[spaceship_name] = 0
            output[spaceship_name] += len(observations)
        with open('summary.txt', 'w') as output_file:
            for spaceship_name, unique_obs_count in output.items():
                output_file.write(f'{spaceship_name}:{unique_obs_count}\n')
    except Exception as e:
        with open('summary.txt', 'w') as output_file:
            pass