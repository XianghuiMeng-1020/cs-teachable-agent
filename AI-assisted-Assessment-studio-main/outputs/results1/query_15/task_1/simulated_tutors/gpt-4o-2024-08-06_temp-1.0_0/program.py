def is_all_ids_unique(file_path):
    unique_ids = set()  # Use a set to store unique IDs, leverages fast lookup times
    with open(file_path, 'r') as file:
        for line in file:
            id = line.strip()  # Strip newline character from each line
            if id in unique_ids:
                return False
            unique_ids.add(id)
    return True

# The program uses file reading, set for uniqueness check, and a for-loop to iterate.
# No selection statements are required beyond the context of the for loop.