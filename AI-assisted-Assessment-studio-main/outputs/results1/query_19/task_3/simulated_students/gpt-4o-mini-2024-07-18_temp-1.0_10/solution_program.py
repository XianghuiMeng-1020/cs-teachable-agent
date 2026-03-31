def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            records = file.readlines()
    except FileNotFoundError:
        with open(output_file, 'w') as out_file:
            out_file.write('Error: Input file not found.')
        return
    except Exception as e:
        with open(output_file, 'w') as out_file:
            out_file.write(f'Error: {str(e)}')
        return

    total_expeditions = 0
    total_crew_members = 0
    years = set()

    for record in records:
        try:
            expedition_id, captain_name, year, crew_members = record.strip().split(',')
            expedition_id = int(expedition_id)
            year = int(year)
            crew_members = int(crew_members)
            total_expeditions += 1
            total_crew_members += crew_members
            years.add(year)
        except ValueError:
            continue

    if total_expeditions == 0:
        average_crew_members = 0.0
    else:
        average_crew_members = total_crew_members / total_expeditions

    report_lines = [
        f'Total number of expeditions: {total_expeditions}',
        f'Total number of crew members: {total_crew_members}',
        f'Average number of crew members per expedition: {average_crew_members:.2f}',
        f'Total number of unique years: {len(years)}'
    ]

    try:
        with open(output_file, 'w') as out_file:
            out_file.write('\n'.join(report_lines))
    except Exception as e:
        with open(output_file, 'w') as out_file:
            out_file.write(f'Error: {str(e)}')