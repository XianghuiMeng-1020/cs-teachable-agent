def sort_creatures_by_realm(creature_data):
    sorted_realm_dict = {}
    for creature, realm in creature_data.items():
        if realm not in sorted_realm_dict:
            sorted_realm_dict[realm] = []
        sorted_realm_dict[realm].append(creature)
    for realm in sorted_realm_dict:
        sorted_realm_dict[realm].sort()
    return sorted_realm_dict