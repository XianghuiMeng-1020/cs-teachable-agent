def extract_entities(file_path):
    heroes = set()
    gods = set()
    creatures = set()
    
    with open(file_path, 'r') as file:
        for line in file:
            story_title, entities = line.strip().split(': ')
            hero_name, god_name, creature_name = map(str.strip, entities.split(','))
            if hero_name:
                heroes.add(hero_name)
            if god_name:
                gods.add(god_name)
            if creature_name:
                creatures.add(creature_name)

    return {
        'heroes': sorted(heroes),
        'gods': sorted(gods),
        'creatures': sorted(creatures)
    }