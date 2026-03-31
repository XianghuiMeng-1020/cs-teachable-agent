def extract_entities(file_path):
    heroes = set()
    gods = set()
    creatures = set()
    
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                story, entities = line.split(':', 1)
                entity_list = entities.split(',')
                
                if len(entity_list) == 3:
                    hero, god, creature = map(str.strip, entity_list)
                    heroes.add(hero)
                    gods.add(god)
                    creatures.add(creature)
    
    return {
        'heroes': sorted(heroes),
        'gods': sorted(gods),
        'creatures': sorted(creatures)
    }