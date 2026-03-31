def mythical_quest(heroes, total_artifacts):
    allocation = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    results = []
    remaining_artifacts = total_artifacts

    for hero in heroes:
        name, rank = hero
        if rank in allocation:
            needed = allocation[rank]
            if remaining_artifacts >= needed:
                results.append((name, needed))
                remaining_artifacts -= needed
            else:
                results.append((name, 0))
        else:
            results.append((name, 0))

    return results