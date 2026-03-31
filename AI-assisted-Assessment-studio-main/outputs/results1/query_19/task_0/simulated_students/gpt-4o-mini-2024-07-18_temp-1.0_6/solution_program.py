def summarize_observations():
    import os
    from collections import defaultdict

    logs_file = 'spaceship_logs.txt'
    summary_file = 'summary.txt'
    observations = defaultdict(set)

    try:
        with open(logs_file, 'r') as file:
            for line in file:
                line = line.strip()  
                if line:
                    spaceship_name, planet_name, observation = line.split(':')
                    observations[(spaceship_name, planet_name)].add(observation)

        with open(summary_file, 'w') as summary:
            for (spaceship_name, planet_name), obs_set in observations.items():
                unique_observations_count = len(obs_set)
                summary.write(f'{spaceship_name}:{unique_observations_count}\n')

    except Exception as e:
        with open(summary_file, 'w') as summary:
            summary.write('')