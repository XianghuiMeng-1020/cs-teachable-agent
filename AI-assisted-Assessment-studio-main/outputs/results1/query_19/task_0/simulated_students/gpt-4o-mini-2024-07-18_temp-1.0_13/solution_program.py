def summarize_observations():
    import os
    from collections import defaultdict

    logs_file = 'spaceship_logs.txt'
    summary_file = 'summary.txt'

    try:
        with open(logs_file, 'r') as f:
            data = f.readlines()
    except Exception as e:
        with open(summary_file, 'w') as f:
            f.write('')  # Create an empty summary file on error
        return

    observations = defaultdict(set)

    for line in data:
        if line.strip():
            spaceship_name, planet_name, observation = line.strip().split(':')
            observations[(spaceship_name, planet_name)].add(observation)

    summary = defaultdict(int)

    for (spaceship_name, planet_name), obs_set in observations.items():
        summary[spaceship_name] += len(obs_set)

    with open(summary_file, 'w') as f:
        for spaceship_name, unique_count in summary.items():
            f.write(f'{spaceship_name}:{unique_count}\n')