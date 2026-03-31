def is_all_ids_unique(file_path):
    id_set = set()
    with open(file_path, 'r') as file:
        for line in file:
            id_str = line.strip()
            if id_str in id_set:
                return False
            id_set.add(id_str)
    return True