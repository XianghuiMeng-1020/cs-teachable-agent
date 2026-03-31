def process_myth_artifacts(artifacts):
    categorized_artifacts = {}
    total_count = {}

    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']

        if myth not in categorized_artifacts:
            categorized_artifacts[myth] = []
            total_count[myth] = 0

        categorized_artifacts[myth].append(name)
        total_count[myth] += 1

    total_artifacts = sum(total_count.values())
    total_count['total'] = total_artifacts

    categorized_artifacts['totals'] = total_count

    return categorized_artifacts