def mythical_quest(heroes, total_artifacts):
    artifacts_distribution = []
    rank_artifacts = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}

    for hero in heroes:
        name, rank = hero
        allocated = 0
        if total_artifacts > 0:
            allocated = min(rank_artifacts[rank], total_artifacts)
            total_artifacts -= allocated
        artifacts_distribution.append((name, allocated))

    return artifacts_distribution