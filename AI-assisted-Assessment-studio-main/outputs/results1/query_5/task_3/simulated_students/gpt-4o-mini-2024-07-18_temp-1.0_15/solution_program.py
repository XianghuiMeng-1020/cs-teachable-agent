def analyze_pantheon():
    try:
        with open('pantheon.txt', 'r') as file:
            gods = []
            total_power = 0
            count = 0

            for line in file:
                name, power = line.strip().split(', ')
                power = int(power)
                gods.append((name, power))
                total_power += power
                count += 1

            if not gods:
                return None  # Handle the case with no gods

            min_god = gods[0]
            max_god = gods[0]

            for god in gods:
                if god[1] < min_god[1]:
                    min_god = god
                if god[1] > max_god[1]:
                    max_god = god

            average_power = total_power // count

            return (min_god[0], max_god[0], average_power)
    except IOError:
        return None
    except Exception as e:
        return None