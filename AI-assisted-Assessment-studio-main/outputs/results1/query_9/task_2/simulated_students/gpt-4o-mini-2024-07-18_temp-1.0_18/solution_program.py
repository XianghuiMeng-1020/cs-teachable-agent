def sort_creatures_by_realm(creature_data):
    realm_creatures = {}
    for creature, realm in creature_data.items():
        if realm not in realm_creatures:
            realm_creatures[realm] = []
        realm_creatures[realm].append(creature)
    for realm in realm_creatures:
        realm_creatures[realm].sort()
    return realm_creatures