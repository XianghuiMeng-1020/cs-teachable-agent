def summarize_observations():
    import os
    from collections import defaultdict

    log_file = 'spaceship_logs.txt'
    summary_file = 'summary.txt'

    observations = defaultdict(set)

    try:
        with open(log_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 3:
                    spaceship, planet, observation = parts
                    observations[spaceship].add((planet, observation))

    except Exception:
        with open(summary_file, 'w') as sf:
            sf.write('')  # Create an empty summary file
        return

    with open(summary_file, 'w') as sf:
        for spaceship, obs_set in observations.items():
            unique_observations_count = len(obs_set)
            sf.write(f'{spaceship}:{unique_observations_count}\n')