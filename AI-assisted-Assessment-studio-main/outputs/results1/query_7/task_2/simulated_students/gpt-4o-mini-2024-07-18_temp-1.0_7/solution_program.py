def generate_hero_list(input_file):
    hero_dict = {}
    with open(input_file, 'r') as file:
        for line in file:
            hero, mythology = line.strip().split(';')
            if mythology not in hero_dict:
                hero_dict[mythology] = []
            hero_dict[mythology].append(hero)
    for mythology in hero_dict:
        hero_dict[mythology] = sorted(hero_dict[mythology])
    return hero_dict