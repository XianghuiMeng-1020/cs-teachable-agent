def process_myth_artifacts(artifacts):
    result = {}
    totals = {}
    total_count = 0

    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']

        if myth not in result:
            result[myth] = []
            totals[myth] = 0

        result[myth].append(name)
        totals[myth] += 1
        total_count += 1

    totals['total'] = total_count
    result['totals'] = totals

    return result