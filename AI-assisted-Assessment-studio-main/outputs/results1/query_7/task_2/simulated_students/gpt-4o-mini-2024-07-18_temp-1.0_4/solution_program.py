def generate_hero_list(input_file):
    hero_dict = {}
    with open(input_file, 'r') as file:
        for line in file:
            hero_name, mythology_type = line.strip().split(';')
            if mythology_type not in hero_dict:
                hero_dict[mythology_type] = []
            hero_dict[mythology_type].append(hero_name)
    for mythology in hero_dict:
        hero_dict[mythology].sort()
    return hero_dict