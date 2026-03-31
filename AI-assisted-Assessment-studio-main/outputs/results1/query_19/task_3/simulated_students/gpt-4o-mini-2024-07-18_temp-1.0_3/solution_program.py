def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            records = infile.readlines()
    except FileNotFoundError:
        with open(output_file, 'w') as outfile:
            outfile.write('Error: Input file not found.')
        return
    except IOError:
        with open(output_file, 'w') as outfile:
            outfile.write('Error: Unable to read the input file.')
        return

    total_expeditions = 0
    total_crew_members = 0
    unique_years = set()

    for record in records:
        record = record.strip()
        if not record:
            continue  # Skip empty lines
        fields = record.split(',')
        if len(fields) != 4:
            continue  # Skip invalid records
        try:
            expedition_id = int(fields[0])
            captain_name = fields[1].strip()
            year = int(fields[2])
            crew_members = int(fields[3])
        except ValueError:
            continue  # Skip records with invalid integer conversion

        total_expeditions += 1
        total_crew_members += crew_members
        unique_years.add(year)

    if total_expeditions > 0:
        average_crew_members = total_crew_members / total_expeditions
    else:
        average_crew_members = 0

    report_lines = [
        f'Total number of expeditions: {total_expeditions}',
        f'Total number of crew members: {total_crew_members}',
        f'Average number of crew members per expedition: {average_crew_members:.2f}',
        f'Total number of unique years: {len(unique_years)}'
    ]

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(report_lines))