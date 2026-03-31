def is_all_ids_unique(file_path):
    ids_seen = set()
    with open(file_path, 'r') as file:
        for line in file:
            galactic_id = line.strip()
            if galactic_id in ids_seen:
                return False
            ids_seen.add(galactic_id)
    return True