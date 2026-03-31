def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        with open(output_file, 'w') as out_file:
            out_file.write('Error: The input file was not found.\n')
        return
    except Exception as e:
        with open(output_file, 'w') as out_file:
            out_file.write(f'Error: {str(e)}\n')
        return

    total_expeditions = 0
    total_crew_members = 0
    unique_years = set()

    for line in lines:
        try:
            parts = line.strip().split(',')
            expedition_id = int(parts[0].strip())
            captain_name = parts[1].strip()
            year = int(parts[2].strip())
            crew_members = int(parts[3].strip())

            total_expeditions += 1
            total_crew_members += crew_members
            unique_years.add(year)

        except (ValueError, IndexError):
            with open(output_file, 'w') as out_file:
                out_file.write('Error: Invalid data format in the input file.\n')
            return

    average_crew_members = total_crew_members / total_expeditions if total_expeditions > 0 else 0
    average_crew_members = round(average_crew_members, 2)

    summary = f'Total number of expeditions: {total_expeditions}\n'
    summary += f'Total number of crew members: {total_crew_members}\n'
    summary += f'Average number of crew members per expedition: {average_crew_members}\n'
    summary += f'Total number of unique years: {len(unique_years)}\n'

    with open(output_file, 'w') as out_file:
        out_file.write(summary)