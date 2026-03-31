def summarize_observations():
    import os
    from collections import defaultdict

    spaceship_data = defaultdict(set)

    try:
        with open('spaceship_logs.txt', 'r') as file:
            for line in file:
                spaceship_name, planet_name, observation = line.strip().split(':')
                # Add unique observation per spaceship and planet
data_key = (spaceship_name, planet_name)
                spaceship_data[data_key].add(observation)

    except Exception as e:
        with open('summary.txt', 'w') as summary_file:
            pass
        return

    summary = defaultdict(int)
    for (spaceship_name, planet_name), observations in spaceship_data.items():
        summary[spaceship_name] += len(observations)

    with open('summary.txt', 'w') as summary_file:
        for spaceship_name, unique_observations in summary.items():
            summary_file.write(f'{spaceship_name}:{unique_observations}\n')
