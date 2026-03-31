def is_all_ids_unique(file_path):
    try:
        with open(file_path, 'r') as file:
            ids = set()
            for line in file:
                galactic_id = line.strip()
                if galactic_id in ids:
                    return False
                ids.add(galactic_id)
        return True
    except IOError:
        return False