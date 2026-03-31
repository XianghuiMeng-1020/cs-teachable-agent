def sort_creatures_by_realm(creature_data):
    realm_dict = {}
    for creature, realm in creature_data.items():
        if realm not in realm_dict:
            realm_dict[realm] = []
        realm_dict[realm].append(creature)
    for creatures in realm_dict.values():
        creatures.sort()
    return realm_dict
