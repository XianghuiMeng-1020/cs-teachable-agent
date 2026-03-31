def pantheon_summary(gods_list):
    summary = {}
    for god in gods_list:
        pantheon = god['pantheon']
        realm = god['realm']
        if pantheon not in summary:
            summary[pantheon] = {'count': 0, 'realms': []}
        summary[pantheon]['count'] += 1
        if realm not in summary[pantheon]['realms']:
            summary[pantheon]['realms'].append(realm)
    for pantheon in summary:
        summary[pantheon]['realms'].sort()
    return summary