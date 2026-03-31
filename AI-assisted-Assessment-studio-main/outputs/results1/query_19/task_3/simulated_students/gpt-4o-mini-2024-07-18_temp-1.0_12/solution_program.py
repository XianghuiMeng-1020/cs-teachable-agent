def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            records = file.readlines()
    except FileNotFoundError:
        with open(output_file, 'w') as f:
            f.write("Error: The input file was not found.")
        return
    except Exception as e:
        with open(output_file, 'w') as f:
            f.write(f"Error: {str(e)}")
        return

    total_expeditions = 0
    total_crew_members = 0
    years = set()

    for record in records:
        try:
            parts = record.strip().split(',')
            expedition_id = int(parts[0])
            captain_name = parts[1].strip()
            year = int(parts[2])
            crew_members = int(parts[3])

            total_expeditions += 1
            total_crew_members += crew_members
            years.add(year)
        except (IndexError, ValueError) as e:
            with open(output_file, 'w') as f:
                f.write("Error: Malformed data in record: '{}'\n".format(record.strip()))
            return

    unique_years_count = len(years)
    average_crew_members = total_crew_members / total_expeditions if total_expeditions > 0 else 0

    with open(output_file, 'w') as f:
        f.write(f"Total Expeditions: {total_expeditions}\n")
        f.write(f"Total Crew Members: {total_crew_members}\n")
        f.write(f"Average Crew Members per Expedition: {average_crew_members:.2f}\n")
        f.write(f"Unique Years of Expeditions: {unique_years_count}\n")