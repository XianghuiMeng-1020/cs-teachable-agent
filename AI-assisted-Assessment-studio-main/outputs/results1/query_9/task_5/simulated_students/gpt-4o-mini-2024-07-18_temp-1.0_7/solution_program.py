def process_myth_artifacts(artifacts):
    categorized_artifacts = {}
    totals = {}

    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']
        
        if myth not in categorized_artifacts:
            categorized_artifacts[myth] = []
            totals[myth] = 0

        categorized_artifacts[myth].append(name)
        totals[myth] += 1

    totals['total'] = sum(totals.values())

    return {**categorized_artifacts, 'totals': totals}