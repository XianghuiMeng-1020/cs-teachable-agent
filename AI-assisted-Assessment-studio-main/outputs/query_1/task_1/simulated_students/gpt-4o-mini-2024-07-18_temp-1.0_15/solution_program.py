def mythical_quest(heroes, total_artifacts):
    rank_to_artifacts = {'Novice': 1, 'Intermediate': 3, 'Advanced': 7}
    allocation = []

    for hero in heroes:
        hero_name, rank = hero
        needed_artifacts = rank_to_artifacts[rank]
        allocation.append((hero_name, min(needed_artifacts, total_artifacts)))
        total_artifacts -= allocation[-1][1]

    return allocation