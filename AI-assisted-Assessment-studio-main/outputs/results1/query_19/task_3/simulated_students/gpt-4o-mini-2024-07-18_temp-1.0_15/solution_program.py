def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()
    except FileNotFoundError:
        error_message = "Error: Input file not found."
        with open(output_file, 'w') as outfile:
            outfile.write(error_message)
        return

    total_expeditions = 0
    total_crew_members = 0
    unique_years = set()

    for line in lines:
        parts = line.strip().split(',')
        if len(parts) != 4:
            continue
        try:
            expedition_id = int(parts[0])
            captain_name = parts[1].strip()
            year = int(parts[2])
            crew_members = int(parts[3])
        except ValueError:
            continue

        total_expeditions += 1
        total_crew_members += crew_members
        unique_years.add(year)

    if total_expeditions == 0:
        avg_crew_members = 0.0
    else:
        avg_crew_members = total_crew_members / total_expeditions

    summary = f'Total Number of Expeditions: {total_expeditions}\n'
    summary += f'Total Number of Crew Members: {total_crew_members}\n'
    summary += f'Average Number of Crew Members per Expedition: {avg_crew_members:.2f}\n'
    summary += f'Total Number of Unique Years: {len(unique_years)}\n'

    with open(output_file, 'w') as outfile:
        outfile.write(summary)