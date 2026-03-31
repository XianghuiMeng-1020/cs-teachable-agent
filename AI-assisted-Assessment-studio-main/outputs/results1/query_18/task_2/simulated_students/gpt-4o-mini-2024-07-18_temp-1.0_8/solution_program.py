def average_energy(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            if not lines:
                return 0
            total = sum(int(line.strip()) for line in lines)
            return total / len(lines)
    except (FileNotFoundError, ValueError):
        return 0