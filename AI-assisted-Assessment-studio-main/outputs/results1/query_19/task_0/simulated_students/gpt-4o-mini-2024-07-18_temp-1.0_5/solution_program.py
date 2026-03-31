def summarize_observations():
    from collections import defaultdict
    import os

    log_file = 'spaceship_logs.txt'
    summary_file = 'summary.txt'
    obj_map = defaultdict(set)  

    try:
        with open(log_file, 'r') as file:
            for line in file:
                spaceship_name, planet_name, observation = line.strip().split(':')
                obj_map[spaceship_name].add((planet_name, observation))  
        with open(summary_file, 'w') as summary:
            for spaceship, observations in obj_map.items():
                summary.write(f'{spaceship}:{len(observations)}\n')
    except Exception:
        with open(summary_file, 'w') as summary:
            summary.write('')