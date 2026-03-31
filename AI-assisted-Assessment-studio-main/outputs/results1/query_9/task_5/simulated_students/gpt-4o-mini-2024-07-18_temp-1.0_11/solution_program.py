def process_myth_artifacts(artifacts):
    myth_dict = {}
    total_dict = {'total': 0}

    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']

        if myth not in myth_dict:
            myth_dict[myth] = []
            total_dict[myth] = 0
        myth_dict[myth].append(name)
        total_dict[myth] += 1
        total_dict['total'] += 1

    myth_dict['totals'] = total_dict
    return myth_dict