def interpret_omens(omens):
    victory_count = sum(1 for omen in omens.values() if omen == 'Victory')
    defeat_count = sum(1 for omen in omens.values() if omen == 'Defeat')
    if victory_count > defeat_count:
        return 'Triumph approaches!'
    elif defeat_count > victory_count:
        return 'Danger looms ahead!'
    else:
        return 'Path is uncertain'