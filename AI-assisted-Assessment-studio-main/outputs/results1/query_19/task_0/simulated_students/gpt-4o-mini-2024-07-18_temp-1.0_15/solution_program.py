def summarize_observations():
    import os
    from collections import defaultdict

    spaceship_observations = defaultdict(set)

    try:
        with open('spaceship_logs.txt', 'r') as logs:
            for line in logs:
                line = line.strip()
                if line:
                    spaceship_name, planet_name, observation = line.split(':')
                    unique_key = (planet_name, observation)
                    spaceship_observations[spaceship_name].add(unique_key)
        
        with open('summary.txt', 'w') as summary:
            for spaceship, observations in spaceship_observations.items():
                summary.write(f'{spaceship}:{len(observations)}\n')
    except IOError:
        with open('summary.txt', 'w') as summary:
            summary.write('')