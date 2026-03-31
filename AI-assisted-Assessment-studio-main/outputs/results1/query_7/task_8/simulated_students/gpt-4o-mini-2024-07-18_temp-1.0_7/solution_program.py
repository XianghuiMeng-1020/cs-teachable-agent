def extract_entities(file_path):
    heroes = set()
    gods = set()
    creatures = set()
    with open(file_path, 'r') as file:
        for line in file:
            story_title, entities = line.strip().split(':')
            hero, god, creature = [e.strip() for e in entities.split(',')]
            heroes.add(hero)
            gods.add(god)
            creatures.add(creature)
    return {
        'heroes': sorted(heroes),
        'gods': sorted(gods),
        'creatures': sorted(creatures)
    }