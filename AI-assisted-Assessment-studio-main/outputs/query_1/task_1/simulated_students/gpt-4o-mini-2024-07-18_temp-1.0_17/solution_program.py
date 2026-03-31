def mythical_quest(heroes, total_artifacts):
    allocation = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    result = []

    for hero, rank in heroes:
        result.append((hero, allocation[rank]))

    for i in range(len(result)):
        hero_name, required_artifacts = result[i]
        if total_artifacts >= required_artifacts:
            result[i] = (hero_name, required_artifacts)
            total_artifacts -= required_artifacts
        else:
            result[i] = (hero_name, total_artifacts)
            total_artifacts = 0

    return result