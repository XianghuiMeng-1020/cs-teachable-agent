import os

def analyze_weather(station_id):
    filename = f"Station{station_id}.txt"
    temperatures = []  # List to store temperatures

    try:
        # File handling
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()  # Remove whitespace and newlines
                try:
                    # Convert line to float and append to list
                    temperatures.append(float(line))
                except ValueError:
                    return "Error: Non-parsable data encountered."

        # Calculate average if list is not empty
        if temperatures:
            average_temp = sum(temperatures) / len(temperatures)
            return round(average_temp, 2)
        else:
            return "Error: No data found in file."

    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"

# The code uses variables, loops for iterating over file lines, exception handling for errors like missing files and non-parsable data, and file handling to read temperatures from files.