def is_all_ids_unique(file_path):
    ids_set = set()
    with open(file_path, 'r') as file:
        for line in file:
            galactic_id = line.strip()
            if galactic_id in ids_set:
                return False
            ids_set.add(galactic_id)
    return True