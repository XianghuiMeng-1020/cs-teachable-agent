def mythical_quest(heroes, total_artifacts):
    rank_to_artifacts = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    allocations = []

    for hero in heroes:
        name, rank = hero
        allocations.append((name, rank_to_artifacts[rank]))

    for i in range(len(allocations)-1, -1, -1):
        if total_artifacts <= 0:
            break
        name, max_allocation = allocations[i]
        if total_artifacts >= max_allocation:
            allocations[i] = (name, max_allocation)
            total_artifacts -= max_allocation
        else:
            allocations[i] = (name, total_artifacts)
            total_artifacts = 0

    return [(hero[0], hero[1]) for hero in allocations]