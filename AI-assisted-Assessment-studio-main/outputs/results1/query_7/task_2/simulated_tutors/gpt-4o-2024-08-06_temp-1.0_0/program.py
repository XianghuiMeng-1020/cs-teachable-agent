def generate_hero_list(input_file):
    heroes_by_mythology = {}
    with open(input_file, 'r') as file:
        for line in file:
            hero, mythology = line.strip().split(';')
            if mythology not in heroes_by_mythology:
                heroes_by_mythology[mythology] = []
            heroes_by_mythology[mythology].append(hero)
    # Sort hero names for each mythology
    for heroes in heroes_by_mythology.values():
        heroes.sort()
    return heroes_by_mythology