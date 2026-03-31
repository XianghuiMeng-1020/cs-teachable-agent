def average_energy(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            if not lines:
                return 0
            total = 0
            count = 0
            for line in lines:
                total += int(line.strip())
                count += 1
            return total / count
    except FileNotFoundError:
        return 0