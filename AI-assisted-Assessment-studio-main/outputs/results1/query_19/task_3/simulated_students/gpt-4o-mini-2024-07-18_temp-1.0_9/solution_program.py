def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
    except IOError:
        with open(output_file, 'w') as out_file:
            out_file.write('Error: Could not access the input file.')
        return

    total_expeditions = 0
    total_crew_members = 0
    unique_years = set()

    for line in lines:
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
            continue  # Skip any malformed lines

    if total_expeditions > 0:
        avg_crew_members = total_crew_members / total_expeditions
    else:
        avg_crew_members = 0

    summary_lines = [
        f'Total number of expeditions: {total_expeditions}',
        f'Total number of crew members: {total_crew_members}',
        f'Average number of crew members per expedition: {avg_crew_members:.2f}',
        f'Total number of unique years: {len(unique_years)}'
    ]

    with open(output_file, 'w') as out_file:
        out_file.write('\n'.join(summary_lines))