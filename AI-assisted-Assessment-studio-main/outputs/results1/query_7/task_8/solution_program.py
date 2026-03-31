def extract_entities(file_path):
    heroes = set()
    gods = set()
    creatures = set()
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(': ')
            if len(parts) == 2:
                entities = parts[1].split(', ')
                if len(entities) == 3:
                    hero, god, creature = entities
                    if hero:
                        heroes.add(hero)
                    if god:
                        gods.add(god)
                    if creature:
                        creatures.add(creature)
    return {
        'heroes': sorted(heroes),
        'gods': sorted(gods),
        'creatures': sorted(creatures)
    }