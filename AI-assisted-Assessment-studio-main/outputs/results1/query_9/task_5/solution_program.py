def process_myth_artifacts(artifacts):
    mythology_dict = {}
    totals = {}
    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']
        if myth not in mythology_dict:
            mythology_dict[myth] = []
            totals[myth] = 0
        mythology_dict[myth].append(name)
        totals[myth] += 1
    total_artifacts = sum(totals.values())
    mythology_dict['totals'] = totals
    mythology_dict['totals']['total'] = total_artifacts
    return mythology_dict
