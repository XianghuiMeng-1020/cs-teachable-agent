def is_all_ids_unique(file_path):
    ids_seen = set()
    with open(file_path, 'r') as f:
        for line in f:
            id_str = line.strip()
            if id_str in ids_seen:
                return False
            ids_seen.add(id_str)
    return True
