def summarize_observations():
    try:
        with open('spaceship_logs.txt', 'r') as infile:
            logs = infile.readlines()
    except Exception:
        open('summary.txt', 'w').close()
        return

    summary = {}

    for log in logs:
        log = log.strip()
        if not log:  
            continue
        spaceship_name, planet_name, observation = log.split(':')
        key = (spaceship_name, planet_name)
        if key not in summary:
            summary[key] = set()
        summary[key].add(observation)

    final_summary = {}

    for (spaceship_name, planet_name), observations in summary.items():
        if spaceship_name not in final_summary:
            final_summary[spaceship_name] = set()
        final_summary[spaceship_name].update(observations)

    with open('summary.txt', 'w') as outfile:
        for spaceship_name, observations in final_summary.items():
            outfile.write(f'{spaceship_name}:{len(observations)}\n')