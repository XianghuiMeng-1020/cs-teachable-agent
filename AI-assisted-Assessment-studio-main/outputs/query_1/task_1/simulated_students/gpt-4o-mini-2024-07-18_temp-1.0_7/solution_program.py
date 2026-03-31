def mythical_quest(heroes, total_artifacts):
    rank_distribution = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    hero_artifacts = []
    remaining_artifacts = total_artifacts

    for hero in heroes:
        hero_name, rank = hero
        artifacts = rank_distribution[rank]
        if remaining_artifacts >= artifacts:
            hero_artifacts.append((hero_name, artifacts))
            remaining_artifacts -= artifacts
        else:
            hero_artifacts.append((hero_name, remaining_artifacts))
            remaining_artifacts = 0

    while remaining_artifacts > 0:
        for i in range(len(hero_artifacts)-1, -1, -1):
            hero_name, allocated = hero_artifacts[i]
            rank = hero[1]
            artifacts = rank_distribution[rank] - allocated
            if artifacts > 0:
                if remaining_artifacts >= artifacts:
                    hero_artifacts[i] = (hero_name, allocated + artifacts)
                    remaining_artifacts -= artifacts
                else:
                    hero_artifacts[i] = (hero_name, allocated + remaining_artifacts)
                    remaining_artifacts = 0
                    break

    return hero_artifacts