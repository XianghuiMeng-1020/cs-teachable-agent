def process_myth_artifacts(artifacts):
    catalog = {}
    total_count = 0
    
    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']
        total_count += 1
        if myth not in catalog:
            catalog[myth] = []
        catalog[myth].append(name)
    
    totals = {myth: len(names) for myth, names in catalog.items()}
    totals['total'] = total_count
    
    catalog['totals'] = totals
    
    return catalog