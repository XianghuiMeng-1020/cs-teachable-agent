def extract_entities(file_path):
    heroes = set()
    gods = set()
    creatures = set()
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) > 1:
                entities = parts[1].split(',')
                if len(entities) == 3:
                    heroes.add(entities[0].strip())
                    gods.add(entities[1].strip())
                    creatures.add(entities[2].strip())
    
    return {
        'heroes': sorted(list(heroes)),
        'gods': sorted(list(gods)),
        'creatures': sorted(list(creatures))
    }