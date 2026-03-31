def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            expedition_records = file.readlines()
    except IOError:
        with open(output_file, 'w') as out_file:
            out_file.write("Error: Unable to read the input file.")
        return

    total_expeditions = 0
    total_crew_members = 0
    unique_years = set()

    for line in expedition_records:
        try:
            parts = line.strip().split(',')
            expedition_id = int(parts[0])
            captain_name = parts[1].strip()
            year = int(parts[2])
            crew_members = int(parts[3])
            total_expeditions += 1
            total_crew_members += crew_members
            unique_years.add(year)
        except (ValueError, IndexError):
            with open(output_file, 'w') as out_file:
                out_file.write("Error: Invalid data in the expedition record: '" + line.strip() + "'.")
            return

    with open(output_file, 'w') as out_file:
        average_crew_members = (total_crew_members / total_expeditions) if total_expeditions > 0 else 0
        out_file.write(f'Total number of expeditions: {total_expeditions}\n')
        out_file.write(f'Total number of crew members: {total_crew_members}\n')
        out_file.write(f'Average number of crew members per expedition: {average_crew_members:.2f}\n')
        out_file.write(f'Total number of unique years: {len(unique_years)}\n')