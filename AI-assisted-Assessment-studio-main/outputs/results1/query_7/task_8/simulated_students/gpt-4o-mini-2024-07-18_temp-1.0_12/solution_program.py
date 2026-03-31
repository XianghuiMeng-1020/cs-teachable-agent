def extract_entities(file_path):
    heroes = set()
    gods = set()
    creatures = set()

    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into title and entities
            parts = line.strip().split(':')
            if len(parts) > 1:
                entities = parts[1].strip().split(',')
                if len(entities) == 3:
                    hero, god, creature = map(str.strip, entities)
                    heroes.add(hero)
                    gods.add(god)
                    creatures.add(creature)

    return {
        'heroes': sorted(heroes),
        'gods': sorted(gods),
        'creatures': sorted(creatures)
    }