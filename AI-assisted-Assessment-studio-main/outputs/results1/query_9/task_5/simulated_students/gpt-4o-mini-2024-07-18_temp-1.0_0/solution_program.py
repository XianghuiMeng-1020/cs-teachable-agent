def process_myth_artifacts(artifacts):
    categorized_artifacts = {}
    total_counts = {}
    total_artifacts = 0

    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']

        if myth not in categorized_artifacts:
            categorized_artifacts[myth] = []
            total_counts[myth] = 0

        categorized_artifacts[myth].append(name)
        total_counts[myth] += 1
        total_artifacts += 1

    categorized_artifacts['totals'] = {**total_counts, 'total': total_artifacts}
    return categorized_artifacts