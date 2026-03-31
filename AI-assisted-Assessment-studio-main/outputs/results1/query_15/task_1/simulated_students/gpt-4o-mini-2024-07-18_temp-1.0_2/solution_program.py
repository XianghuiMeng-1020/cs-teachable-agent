def is_all_ids_unique(file_path):
    with open(file_path, 'r') as file:
        seen_ids = set()
        for line in file:
            galactic_id = line.strip()
            if galactic_id in seen_ids:
                return False
            seen_ids.add(galactic_id)
    return True