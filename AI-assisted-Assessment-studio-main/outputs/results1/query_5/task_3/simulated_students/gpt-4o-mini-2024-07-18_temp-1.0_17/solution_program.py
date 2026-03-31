def analyze_pantheon():
    min_name = max_name = None
    min_power = float('inf')
    max_power = -float('inf')
    total_power = 0
    count = 0

    try:
        with open('pantheon.txt', 'r') as file:
            for line in file:
                name, power_str = line.strip().split(',')
                power = int(power_str)
                
                if power < min_power:
                    min_power = power
                    min_name = name
                if power > max_power:
                    max_power = power
                    max_name = name
                
                total_power += power
                count += 1
        
    except IOError:
        return None
    except ValueError:
        return None

    average_power = total_power // count
    return (min_name, max_name, average_power)