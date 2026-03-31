def sort_creatures_by_realm(creature_data):
    # Initialize an empty dictionary to hold the sorted creatures by realm
    realm_dict = {}
    
    # Iterate over each creature and its realm in the input dictionary
    for creature, realm in creature_data.items():
        # If the realm is not already a key in the realm_dict, create it
        if realm not in realm_dict:
            realm_dict[realm] = []
        # Append the creature to the list corresponding to its realm
        realm_dict[realm].append(creature)
    
    # Sort the list of creatures for each realm
    for realm in realm_dict:
        realm_dict[realm].sort()
    
    return realm_dict
