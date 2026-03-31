def extract_entities(file_path):
    heroes = set()
    gods = set()
    creatures = set()

    with open(file_path, 'r') as file:
        for line in file:
            story = line.strip().split(':')
            if len(story) > 1:
                entities = story[1].split(',')
                if len(entities) == 3:
                    hero, god, creature = [entity.strip() for entity in entities]
                    heroes.add(hero)
                    gods.add(god)
                    creatures.add(creature)

    return {
        'heroes': sorted(heroes),
        'gods': sorted(gods),
        'creatures': sorted(creatures)
    }