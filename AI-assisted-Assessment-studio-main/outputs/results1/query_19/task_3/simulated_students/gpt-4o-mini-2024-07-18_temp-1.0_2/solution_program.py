def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()
    except Exception as e:
        with open(output_file, 'w') as outfile:
            outfile.write(f'Error reading file: {str(e)}')
        return

    total_expeditions = 0
    total_crew_members = 0
    unique_years = set()

    for line in lines:
        parts = line.strip().split(',')
        if len(parts) != 4:
            continue  # Skip invalid lines

        try:
            expedition_id = int(parts[0])
            captain_name = parts[1].strip()
            year = int(parts[2])
            crew_members = int(parts[3])
        except ValueError:
            continue  # Skip lines with parsing errors

        total_expeditions += 1
        total_crew_members += crew_members
        unique_years.add(year)

    average_crew_members = (total_crew_members / total_expeditions) if total_expeditions > 0 else 0

    summary = f"Total Expeditions: {total_expeditions}\n" + \
              f"Total Crew Members: {total_crew_members}\n" + \
              f"Average Crew Members per Expedition: {average_crew_members:.2f}\n" + \
              f"Unique Years of Expeditions: {len(unique_years)}\n"

    with open(output_file, 'w') as outfile:
        outfile.write(summary)