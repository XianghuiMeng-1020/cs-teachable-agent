def mythical_quest(heroes, total_artifacts):
    rank_distribution = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    artifacts_allocation = []

    for hero_name, rank in heroes:
        allocation = rank_distribution[rank]
        artifacts_allocation.append((hero_name, min(allocation, total_artifacts)))
        total_artifacts -= min(allocation, total_artifacts)

    for i in range(len(artifacts_allocation)-1, -1, -1):
        hero_name, received = artifacts_allocation[i]
        if received < rank_distribution[heroes[i][1]]:
            needed = rank_distribution[heroes[i][1]] - received
            if total_artifacts >= needed:
                artifacts_allocation[i] = (hero_name, received + needed)
                total_artifacts -= needed
            else:
                artifacts_allocation[i] = (hero_name, received + total_artifacts)
                total_artifacts = 0

    return artifacts_allocation