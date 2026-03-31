def mythical_quest(heroes, total_artifacts):
    rank_allocation = {
        'Novice': 1,
        'Intermediate': 3,
        'Advanced': 7
    }
    allocation_results = []

    for hero in heroes:
        hero_name, rank = hero
        allocation_results.append((hero_name, rank_allocation[rank]))

    for i in range(len(allocation_results)):
        hero_name, max_allocation = allocation_results[i]
        if total_artifacts >= max_allocation:
            allocation_results[i] = (hero_name, max_allocation)
            total_artifacts -= max_allocation
        else:
            allocation_results[i] = (hero_name, total_artifacts)
            total_artifacts = 0
            break

    for j in range(i + 1, len(allocation_results)):
        hero_name, _ = allocation_results[j]
        allocation_results[j] = (hero_name, 0)

    return allocation_results