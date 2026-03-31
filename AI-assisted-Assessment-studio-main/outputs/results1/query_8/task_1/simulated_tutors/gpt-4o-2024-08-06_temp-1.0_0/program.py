def interpret_omens(omens):
    # Initialize counters for each omen type
    victory_count = 0
    defeat_count = 0
    
    # Iterate over the dictionary of omens
    for omen in omens.values():
        if omen == 'Victory':
            victory_count += 1
        elif omen == 'Defeat':
            defeat_count += 1

    # Determine the overall outcome based on the omens
    if victory_count > defeat_count:
        return "Triumph approaches!"
    elif defeat_count > victory_count:
        return "Danger looms ahead!"
    else:
        return "Path is uncertain"