def mythical_quest(heroes, total_artifacts):
    rank_to_allocation = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    allocations = []
    remaining_artifacts = total_artifacts

    for hero in heroes:
        hero_name, rank = hero
        allocation = rank_to_allocation[rank]
        if remaining_artifacts >= allocation:
            allocations.append((hero_name, allocation))
            remaining_artifacts -= allocation
        else:
            allocations.append((hero_name, remaining_artifacts))
            remaining_artifacts = 0

    return allocations