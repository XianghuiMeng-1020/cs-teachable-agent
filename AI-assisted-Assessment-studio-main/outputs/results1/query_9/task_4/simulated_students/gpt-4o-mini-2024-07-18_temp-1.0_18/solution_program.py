def pantheon_summary(gods_list):
    summary = {}
    
    for god in gods_list:
        pantheon = god['pantheon']
        realm = god['realm']
        
        if pantheon not in summary:
            summary[pantheon] = {'count': 0, 'realms': set()}
        
        summary[pantheon]['count'] += 1
        summary[pantheon]['realms'].add(realm)
    
    for pantheon in summary:
        summary[pantheon]['realms'] = sorted(summary[pantheon]['realms'])
    
    return summary