def mythical_quest(heroes, total_artifacts):
    rank_to_artifacts = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    artifacts_allocated = []

    for hero_name, rank in heroes:
        allocated = rank_to_artifacts[rank]  
        if total_artifacts >= allocated:
            artifacts_allocated.append((hero_name, allocated))
            total_artifacts -= allocated
        else:
            artifacts_allocated.append((hero_name, 0))

    for i in range(len(artifacts_allocated)-1, -1, -1):
        if total_artifacts <= 0:
            break
        hero_name, current_allocation = artifacts_allocated[i]
        rank = heroes[i][1]
        max_allocation = rank_to_artifacts[rank]  
        if current_allocation < max_allocation:
            additional_allocation = min(max_allocation - current_allocation, total_artifacts)
            artifacts_allocated[i] = (hero_name, current_allocation + additional_allocation)
            total_artifacts -= additional_allocation

    return artifacts_allocated