def interpret_omens(omens):
    victory_count = 0
    defeat_count = 0

    for omen in omens.values():
        if omen == "Victory":
            victory_count += 1
        elif omen == "Defeat":
            defeat_count += 1

    if victory_count > defeat_count:
        return "Triumph approaches!"
    elif defeat_count > victory_count:
        return "Danger looms ahead!"
    else:
        return "Path is uncertain"