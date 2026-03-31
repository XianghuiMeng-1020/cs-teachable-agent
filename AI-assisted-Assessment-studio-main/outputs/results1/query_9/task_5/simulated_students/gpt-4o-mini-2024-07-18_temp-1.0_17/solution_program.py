def process_myth_artifacts(artifacts):
    myth_categories = {}
    total_count = {'total': 0}

    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']
        total_count['total'] += 1

        if myth not in myth_categories:
            myth_categories[myth] = []
            total_count[myth] = 0

        myth_categories[myth].append(name)
        total_count[myth] += 1

    myth_categories['totals'] = total_count
    return myth_categories