def process_myth_artifacts(artifacts):
    result = {}
    totals = {}

    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']

        if myth not in result:
            result[myth] = []
            totals[myth] = 0

        result[myth].append(name)
        totals[myth] += 1

    totals['total'] = sum(totals.values())
    result['totals'] = totals

    return result