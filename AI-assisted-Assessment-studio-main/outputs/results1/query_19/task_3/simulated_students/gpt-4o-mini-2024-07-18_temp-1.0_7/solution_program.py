def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            records = f.readlines()
    except IOError:
        with open(output_file, 'w') as f:
            f.write('Error: Unable to access the input file.')
        return

    total_expeditions = 0
    total_crew_members = 0
    unique_years = set()

    for record in records:
        try:
            expedition_id, captain, year, crew_members = record.strip().split(',')
            expedition_id = int(expedition_id)
            year = int(year)
            crew_members = int(crew_members)
            total_expeditions += 1
            total_crew_members += crew_members
            unique_years.add(year)
        except (ValueError, IndexError):
            continue

    if total_expeditions > 0:
        average_crew_members = round(total_crew_members / total_expeditions, 2)
    else:
        average_crew_members = 0.00

    with open(output_file, 'w') as f:
        f.write(f'Total number of expeditions: {total_expeditions}\n')
        f.write(f'Total number of crew members: {total_crew_members}\n')
        f.write(f'Average number of crew members per expedition: {average_crew_members}\n')
        f.write(f'Total number of unique years: {len(unique_years)}\n')
