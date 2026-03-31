def process_myth_artifacts(artifacts):
    myth_dict = {}
    total_count = 0

    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']
        total_count += 1
        if myth not in myth_dict:
            myth_dict[myth] = []
        myth_dict[myth].append(name)

    myth_dict['totals'] = {myth: len(names) for myth, names in myth_dict.items()}
    myth_dict['totals']['total'] = total_count

    return myth_dict