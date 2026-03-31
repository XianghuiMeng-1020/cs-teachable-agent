def process_myth_artifacts(artifacts):
    myth_dict = {}
    total_artifacts = 0

    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']

        if myth not in myth_dict:
            myth_dict[myth] = []
        myth_dict[myth].append(name)
        total_artifacts += 1

    totals = {myth: len(myth_dict[myth]) for myth in myth_dict}
    totals['total'] = total_artifacts
    myth_dict['totals'] = totals

    return myth_dict
