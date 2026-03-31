def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            expeditions = f.readlines()
    except FileNotFoundError:
        with open(output_file, 'w') as f:
            f.write('Error: Input file not found.')
        return
    except Exception as e:
        with open(output_file, 'w') as f:
            f.write(f'Error: {str(e)}')
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
        except (ValueError, IndexError):
            continue

    average_crew_members = (total_crew_members / total_expeditions) if total_expeditions > 0 else 0
    average_crew_members = round(average_crew_members, 2)

    summary = f'Total Expeditions: {total_expeditions}\n'
    summary += f'Total Crew Members: {total_crew_members}\n'
    summary += f'Average Crew Members per Expedition: {average_crew_members}\n'
    summary += f'Total Unique Years: {len(unique_years)}\n'

    with open(output_file, 'w') as f:
        f.write(summary)