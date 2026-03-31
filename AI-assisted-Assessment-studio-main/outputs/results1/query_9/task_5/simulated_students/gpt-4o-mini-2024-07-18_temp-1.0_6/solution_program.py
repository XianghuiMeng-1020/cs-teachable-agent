def process_myth_artifacts(artifacts):
    myth_dict = {}
    total_count = {}
    total_artifacts = 0
    
    for artifact in artifacts:
        myth = artifact['myth']
        name = artifact['name']
        
        if myth not in myth_dict:
            myth_dict[myth] = []
            total_count[myth] = 0
        
        myth_dict[myth].append(name)
        total_count[myth] += 1
        total_artifacts += 1
    
    myth_dict['totals'] = {**total_count, 'total': total_artifacts}
    
    return myth_dict