def mythical_quest(heroes, total_artifacts):
    rank_to_artifacts = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    artifacts_allocated = []

    for hero in heroes:
        name, rank = hero
        artifacts = rank_to_artifacts[rank]
        allocated = min(artifacts, total_artifacts)
        artifacts_allocated.append((name, allocated))
        total_artifacts -= allocated

    return artifacts_allocated