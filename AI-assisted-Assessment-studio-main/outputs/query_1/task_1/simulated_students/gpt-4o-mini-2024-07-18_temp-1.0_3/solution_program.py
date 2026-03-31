def mythical_quest(heroes, total_artifacts):
    rank_allocation = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    result = []

    for hero in heroes:
        hero_name, rank = hero
        allocated = rank_allocation[rank]
        if total_artifacts >= allocated:
            result.append((hero_name, allocated))
            total_artifacts -= allocated
        else:
            result.append((hero_name, 0))

    for i in range(len(result) - 1, -1, -1):
        if total_artifacts > 0:
            hero_name, current_allocation = result[i]
            rank = heroes[i][1]
            max_allocation = rank_allocation[rank]
            additional_allocation = min(max_allocation - current_allocation, total_artifacts)
            result[i] = (hero_name, current_allocation + additional_allocation)
            total_artifacts -= additional_allocation

    return result