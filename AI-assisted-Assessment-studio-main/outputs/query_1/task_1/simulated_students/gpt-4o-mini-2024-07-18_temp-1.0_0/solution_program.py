def mythical_quest(heroes, total_artifacts):
    allocation = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    result = []
    remaining_artifacts = total_artifacts

    for hero in heroes:
        name, rank = hero
        allocated = allocation[rank]

        if remaining_artifacts >= allocated:
            result.append((name, allocated))
            remaining_artifacts -= allocated
        else:
            result.append((name, remaining_artifacts))
            remaining_artifacts = 0

    return result