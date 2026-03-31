def summarize_observations():
    import os
    from collections import defaultdict

    logs_file = 'spaceship_logs.txt'
    summary_file = 'summary.txt'
    observations = defaultdict(set)

    try:
        with open(logs_file, 'r') as f:
            for line in f:
                if line.strip():  # Ignore empty lines
                    spaceship, planet, observation = line.strip().split(':')
                    observations[spaceship].add((planet, observation))
    except Exception:
        open(summary_file, 'w').close()  # Create an empty summary file
        return

    with open(summary_file, 'w') as f:
        for spaceship, unique_obs in observations.items():
            f.write(f"{spaceship}:{len(unique_obs)}\n")