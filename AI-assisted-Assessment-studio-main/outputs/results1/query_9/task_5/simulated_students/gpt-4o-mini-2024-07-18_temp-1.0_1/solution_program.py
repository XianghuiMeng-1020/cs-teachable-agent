def process_myth_artifacts(artifacts):
    categorized_artifacts = {}
    totals = {}
    total_count = 0

    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']

        if myth not in categorized_artifacts:
            categorized_artifacts[myth] = []
            totals[myth] = 0

        categorized_artifacts[myth].append(name)
        totals[myth] += 1
        total_count += 1

    totals['total'] = total_count
    categorized_artifacts['totals'] = totals

    return categorized_artifacts