def mythical_quest(heroes, total_artifacts):
    rank_allocation = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    allocated = []

    for hero in heroes:
        hero_name, rank = hero
        if rank in rank_allocation:
            num_artifacts = rank_allocation[rank]
        else:
            num_artifacts = 0
        allocated.append((hero_name, num_artifacts))

    total_distributed = 0
    for i in range(len(allocated)):
        if total_distributed < total_artifacts:
            hero_name, requested = allocated[i]
            if total_distributed + requested <= total_artifacts:
                allocated[i] = (hero_name, requested)
                total_distributed += requested
            else:
                allowed = total_artifacts - total_distributed
                allocated[i] = (hero_name, allowed)
                total_distributed += allowed 
        else:
            hero_name = allocated[i][0]
            allocated[i] = (hero_name, 0)

    return allocated