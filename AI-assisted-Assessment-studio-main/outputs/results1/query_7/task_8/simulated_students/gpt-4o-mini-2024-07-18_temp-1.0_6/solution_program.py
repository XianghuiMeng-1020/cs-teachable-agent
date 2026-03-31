def extract_entities(file_path):
    heroes = set()
    gods = set()
    creatures = set()

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(': ')
            if len(parts) > 1:
                entities = parts[1].split(', ')
                if len(entities) == 3:
                    heroes.add(entities[0])
                    gods.add(entities[1])
                    creatures.add(entities[2])

    return {
        'heroes': sorted(heroes),
        'gods': sorted(gods),
        'creatures': sorted(creatures)
    }