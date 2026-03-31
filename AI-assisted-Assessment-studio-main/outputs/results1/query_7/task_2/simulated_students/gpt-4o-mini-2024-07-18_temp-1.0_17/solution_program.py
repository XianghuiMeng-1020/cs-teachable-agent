def generate_hero_list(input_file):
    hero_dict = {}
    with open(input_file, 'r') as file:
        for line in file:
            hero, mythology = line.strip().split(';')
            if mythology in hero_dict:
                hero_dict[mythology].append(hero)
            else:
                hero_dict[mythology] = [hero]
    for mythology in hero_dict:
        hero_dict[mythology].sort()
    return hero_dict