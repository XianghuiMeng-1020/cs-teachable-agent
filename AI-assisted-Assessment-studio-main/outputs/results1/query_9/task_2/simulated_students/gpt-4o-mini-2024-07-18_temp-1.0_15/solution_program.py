def sort_creatures_by_realm(creature_data):
    realms = {}
    for creature, realm in creature_data.items():
        if realm not in realms:
            realms[realm] = []
        realms[realm].append(creature)
    for realm in realms:
        realms[realm].sort()
    return realms