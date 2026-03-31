def mythical_quest(heroes, total_artifacts):
    rank_allocation = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    allocated = []
    for hero in heroes:
        name, rank = hero
        if total_artifacts >= rank_allocation[rank]:
            allocated.append((name, rank_allocation[rank]))
            total_artifacts -= rank_allocation[rank]
        else:
            allocated.append((name, 0))
    return allocated