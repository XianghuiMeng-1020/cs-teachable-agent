def mythical_quest(heroes, total_artifacts):
    rank_to_artifacts = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    results = []

    for hero in heroes:
        hero_name, rank = hero
        allocated_artifacts = rank_to_artifacts[rank]
        results.append((hero_name, allocated_artifacts))

    for i in range(len(results)):
        hero_name, artifacts = results[i]
        if total_artifacts >= artifacts:
            results[i] = (hero_name, artifacts)
            total_artifacts -= artifacts
        else:
            results[i] = (hero_name, total_artifacts)
            total_artifacts = 0
            break

    for j in range(i + 1, len(results)):
        hero_name, artifacts = results[j]
        results[j] = (hero_name, 0)

    return results