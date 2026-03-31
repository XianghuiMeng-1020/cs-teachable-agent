def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            expeditions = file.readlines()
    except IOError:
        with open(output_file, 'w') as out_file:
            out_file.write("Error: Unable to read the input file.\n")
        return

    total_expeditions = 0
    total_crew_members = 0
    unique_years = set()

    for line in expeditions:
        try:
            parts = line.strip().split(',')
            expedition_id = int(parts[0])
            captain_name = parts[1].strip()
            year = int(parts[2])
            crew_members = int(parts[3])

            total_expeditions += 1
            total_crew_members += crew_members
            unique_years.add(year)
        except (IndexError, ValueError):
            with open(output_file, 'w') as out_file:
                out_file.write("Error: Data format issue in input file.\n")
            return

    if total_expeditions == 0:
        avg_crew_members = 0
    else:
        avg_crew_members = total_crew_members / total_expeditions

    try:
        with open(output_file, 'w') as out_file:
            out_file.write(f"Total Number of Expeditions: {total_expeditions}\n")
            out_file.write(f"Total Number of Crew Members: {total_crew_members}\n")
            out_file.write(f"Average Number of Crew Members per Expedition: {avg_crew_members:.2f}\n")
            out_file.write(f"Total Unique Years of Expeditions: {len(unique_years)}\n")
    except IOError:
        with open(output_file, 'w') as out_file:
            out_file.write("Error: Unable to write to the output file.\n")