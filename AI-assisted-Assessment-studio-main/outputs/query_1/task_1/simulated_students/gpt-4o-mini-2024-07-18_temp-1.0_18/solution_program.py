def mythical_quest(heroes, total_artifacts):
    artifact_distribution = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    results = []
    remaining_artifacts = total_artifacts

    sorted_heroes = sorted(heroes, key=lambda x: ('Novice', 'Intermediate', 'Advanced').index(x[1]))

    for hero, rank in sorted_heroes:
        allocation = artifact_distribution[rank]
        if remaining_artifacts >= allocation:
            results.append((hero, allocation))
            remaining_artifacts -= allocation
        else:
            results.append((hero, remaining_artifacts))
            remaining_artifacts = 0

    final_results = []
    for hero in heroes:
        final_results.append((hero[0], next((res[1] for res in results if res[0] == hero[0]), 0)))

    return final_results