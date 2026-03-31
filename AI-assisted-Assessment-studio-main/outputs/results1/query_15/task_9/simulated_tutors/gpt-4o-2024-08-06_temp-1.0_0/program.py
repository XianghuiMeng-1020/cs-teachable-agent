def count_creature_types(creatures):
    # Create an empty dictionary to hold counts of each creature type
    creature_counts = {}
    
    # Loop over each creature in the list
    for creature in creatures:
        # If the creature type is already in the dictionary, increment its count
        if creature in creature_counts:
            creature_counts[creature] += 1
        # If it's not already in the dictionary, add it with an initial count of 1
        else:
            creature_counts[creature] = 1
    
    # Return the dictionary with creature types and counts
    return creature_counts