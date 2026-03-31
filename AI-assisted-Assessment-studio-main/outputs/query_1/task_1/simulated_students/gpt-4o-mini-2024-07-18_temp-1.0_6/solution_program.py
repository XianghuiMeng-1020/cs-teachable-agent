def mythical_quest(heroes, total_artifacts):
    rank_to_artifacts = {
        'Novice': 1,
        'Intermediate': 3,
        'Advanced': 7
    }
    allocation = []

    for hero in heroes:
        name, rank = hero
        artifacts = rank_to_artifacts[rank]
        allocation.append((name, artifacts))

    for i in range(len(allocation)):
        name, required_artifacts = allocation[i]
        if total_artifacts >= required_artifacts:
            allocation[i] = (name, required_artifacts)
            total_artifacts -= required_artifacts
        else:
            allocation[i] = (name, total_artifacts)
            total_artifacts = 0
            break

    for j in range(i + 1, len(allocation)):
        name = allocation[j][0]
        allocation[j] = (name, 0)

    return allocation