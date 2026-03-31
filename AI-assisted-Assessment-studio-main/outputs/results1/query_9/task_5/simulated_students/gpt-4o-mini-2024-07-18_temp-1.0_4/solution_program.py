def process_myth_artifacts(artifacts):
    myth_dict = {}
    total_counts = {}

    for artifact in artifacts:
        name = artifact['name']
        myth = artifact['myth']

        if myth not in myth_dict:
            myth_dict[myth] = []
            total_counts[myth] = 0
        myth_dict[myth].append(name)
        total_counts[myth] += 1

    total_counts['total'] = sum(total_counts.values())

    return {**myth_dict, 'totals': total_counts}