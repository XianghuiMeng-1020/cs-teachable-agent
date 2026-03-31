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
                    spaceship, planet, observation = line.split(':', 2)
                    observations[(spaceship, planet)].add(observation)
    except Exception:
        open(summary_file, 'w').close()
        return

    summary = defaultdict(int)
    for (spaceship, planet), obs_set in observations.items():
        summary[spaceship] += len(obs_set)

    with open(summary_file, 'w') as file:
        for spaceship, unique_count in summary.items():
            file.write(f'{spaceship}:{unique_count}\n')