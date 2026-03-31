def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            records = file.readlines()
    except FileNotFoundError:
        with open(output_file, 'w') as output:
            output.write("Error: Input file not found.")
        return
    except Exception as e:
        with open(output_file, 'w') as output:
            output.write(f"Error: {str(e)}")
        return

    total_expeditions = 0
    total_crew_members = 0
    unique_years = set()

    for line in records:
        try:
            parts = line.strip().split(',')
            expedition_id = int(parts[0])
            captain = parts[1].strip()
            year = int(parts[2])
            crew_members = int(parts[3])

            total_expeditions += 1
            total_crew_members += crew_members
            unique_years.add(year)
        except (ValueError, IndexError):
            continue

    if total_expeditions > 0:
        average_crew_members = round(total_crew_members / total_expeditions, 2)
    else:
        average_crew_members = 0.00

    summary = f"Total Expeditions: {total_expeditions}\n" 
    summary += f"Total Crew Members: {total_crew_members}\n"
    summary += f"Average Crew Members per Expedition: {average_crew_members}\n"
    summary += f"Unique Years: {len(unique_years)}\n"

    try:
        with open(output_file, 'w') as output:
            output.write(summary)
    except Exception as e:
        with open(output_file, 'w') as output:
            output.write(f"Error: {str(e)}")