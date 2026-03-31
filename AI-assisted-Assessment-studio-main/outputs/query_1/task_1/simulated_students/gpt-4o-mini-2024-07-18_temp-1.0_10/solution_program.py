def mythical_quest(heroes, total_artifacts):
    rank_to_artifacts = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    allocations = []
    available_artifacts = total_artifacts

    for hero_name, rank in heroes:
        if available_artifacts <= 0:
            allocations.append((hero_name, 0))
            continue
        artifacts = rank_to_artifacts[rank]
        allocated = min(artifacts, available_artifacts)
        allocations.append((hero_name, allocated))
        available_artifacts -= allocated

    return allocations