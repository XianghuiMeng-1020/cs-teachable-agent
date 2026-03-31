def mythical_quest(heroes, total_artifacts):
    allocation = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    artifacts_allocated = []
    remaining_artifacts = total_artifacts

    for hero in heroes:
        name, rank = hero
        requested = allocation[rank]
        allocated = min(requested, remaining_artifacts)
        artifacts_allocated.append((name, allocated))
        remaining_artifacts -= allocated

    return artifacts_allocated