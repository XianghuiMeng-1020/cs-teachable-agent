def is_all_ids_unique(file_path):
    unique_ids = set()
    with open(file_path, 'r') as file:
        for line in file:
            galactic_id = line.strip()
            if galactic_id in unique_ids:
                return False
            unique_ids.add(galactic_id)
    return True