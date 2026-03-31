def extract_entities(file_path):
    heroes = set()
    gods = set()
    creatures = set()

    with open(file_path, 'r') as file:
        for line in file:
            title, entities = line.strip().split(': ')
            hero, god, creature = entities.split(', ')
            heroes.add(hero)
            gods.add(god)
            creatures.add(creature)

    return {
        'heroes': sorted(heroes),
        'gods': sorted(gods),
        'creatures': sorted(creatures)
    }