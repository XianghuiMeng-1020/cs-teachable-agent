def process_myth_artifacts(artifacts):
    categorized_artifacts = {}
    total_count = {}
    total_artifacts = 0

    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']

        if myth not in categorized_artifacts:
            categorized_artifacts[myth] = []
            total_count[myth] = 0

        categorized_artifacts[myth].append(name)
        total_count[myth] += 1
        total_artifacts += 1

    categorized_artifacts['totals'] = {**total_count, 'total': total_artifacts}
    return categorized_artifacts