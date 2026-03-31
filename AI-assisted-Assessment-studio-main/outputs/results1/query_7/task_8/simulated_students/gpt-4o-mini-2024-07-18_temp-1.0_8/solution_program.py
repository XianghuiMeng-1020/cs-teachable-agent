def extract_entities(file_path):
    heroes = set()
    gods = set()
    creatures = set()

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) != 2:
                continue
            entities = parts[1].strip().split(',')
            if len(entities) != 3:
                continue
            hero, god, creature = [entity.strip() for entity in entities]
            heroes.add(hero)
            gods.add(god)
            creatures.add(creature)

    return {
        'heroes': sorted(heroes),
        'gods': sorted(gods),
        'creatures': sorted(creatures)
    }