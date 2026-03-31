def analyze_pantheon():
    min_name = None
    max_name = None
    total_power = 0
    count = 0

    try:
        with open('pantheon.txt', 'r') as file:
            for line in file:
                name, power_str = line.strip().split(',')
                power = int(power_str)

                if min_name is None or power < min_power:
                    min_power = power
                    min_name = name
                if max_name is None or power > max_power:
                    max_power = power
                    max_name = name

                total_power += power
                count += 1

        average_power = total_power // count
        return (min_name, max_name, average_power)

    except IOError:
        return (None, None, None)
    except ValueError:
        return (None, None, None)