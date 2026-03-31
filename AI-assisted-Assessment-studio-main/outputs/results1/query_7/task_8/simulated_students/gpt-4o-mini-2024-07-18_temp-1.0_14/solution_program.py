def extract_entities(file_path):
    heroes = set()
    gods = set()
    creatures = set()
    
    with open(file_path, 'r') as file:
        for line in file:
            title, entities = line.split(':', 1)
            hero_name, god_name, creature_name = map(str.strip, entities.split(','))
            heroes.add(hero_name)
            gods.add(god_name)
            creatures.add(creature_name)
    
    return {
        'heroes': sorted(heroes),
        'gods': sorted(gods),
        'creatures': sorted(creatures)
    }