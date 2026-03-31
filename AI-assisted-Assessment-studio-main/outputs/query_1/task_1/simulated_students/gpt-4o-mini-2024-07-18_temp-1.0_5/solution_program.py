def mythical_quest(heroes, total_artifacts):
    rank_allocation = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    allocations = []
    remaining_artifacts = total_artifacts

    for hero in heroes:
        name, rank = hero
        max_allocation = rank_allocation[rank]
        if remaining_artifacts >= max_allocation:
            allocations.append((name, max_allocation))
            remaining_artifacts -= max_allocation
        else:
            allocations.append((name, remaining_artifacts))
            remaining_artifacts = 0

    return allocations