def process_myth_artifacts(artifacts):
    result = {}
    total_counts = {}

    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']

        if myth not in result:
            result[myth] = []
            total_counts[myth] = 0

        result[myth].append(name)
        total_counts[myth] += 1

    total_counts['total'] = sum(total_counts.values())
    result['totals'] = total_counts

    return result