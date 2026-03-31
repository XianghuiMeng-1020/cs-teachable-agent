def extract_entities(file_path):
    heroes = set()
    gods = set()
    creatures = set()

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) != 2:
                continue
            _, entities = parts
            hero, god, creature = [e.strip() for e in entities.split(',')]
            heroes.add(hero)
            gods.add(god)
            creatures.add(creature)

    return {
        'heroes': sorted(heroes),
        'gods': sorted(gods),
        'creatures': sorted(creatures)
    }