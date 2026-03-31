def calculate_power(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read().strip()
            if not content:  # Handle empty file
                return 1000
            # Split the content based on commas and strip any whitespace
            changes = map(int, content.split(','))
            # Sum the changes and add to initial power level
            final_power = 1000 + sum(changes)
            return final_power
    except FileNotFoundError:
        print("Error: The file was not found.")
        return None
    except ValueError:
        print("Error: File contains invalid data.")
        return None