def analyze_pantheon():
    import os
    try:
        if os.path.exists('pantheon.txt'):
            with open('pantheon.txt', 'r') as file:
                lines = file.readlines()

            min_power = float('inf')
            max_power = float('-inf')
            min_name = None
            max_name = None
            power_sum = 0
            count = 0

            for line in lines:
                name, power = line.strip().split(",")
                power = int(power)

                if power < min_power:
                    min_power = power
                    min_name = name

                if power > max_power:
                    max_power = power
                    max_name = name

                power_sum += power
                count += 1

            average_power = power_sum // count  # Integer division for flooring

            return (min_name, max_name, average_power)

    except Exception as e:
        print("Error encountered while processing pantheon data:", e)
        return None

# Test the function
print(analyze_pantheon())