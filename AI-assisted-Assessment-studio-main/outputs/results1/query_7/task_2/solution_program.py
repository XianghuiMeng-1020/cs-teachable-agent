def generate_hero_list(input_file):
    heroes_dict = {}
    with open(input_file, 'r') as file:
        for line in file:
            hero, mythology = line.strip().split(';')
            if mythology not in heroes_dict:
                heroes_dict[mythology] = []
            heroes_dict[mythology].append(hero)
    for heroes in heroes_dict.values():
        heroes.sort()
    return heroes_dict