def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            expeditions = file.readlines()
    except FileNotFoundError:
        with open(output_file, 'w') as out_file:
            out_file.write("Error: The input file was not found.")
        return
    except Exception as e:
        with open(output_file, 'w') as out_file:
            out_file.write(f"Error: An error occurred while accessing the file - {str(e)}")
        return

    total_expeditions = 0
    total_crew_members = 0
    unique_years = set()

    for record in expeditions:
        fields = record.strip().split(',')
        if len(fields) != 4:
            continue
        try:
            expedition_id = int(fields[0])
            captain_name = fields[1].strip()
            year = int(fields[2])
            crew_members = int(fields[3])
        except ValueError:
            continue

        total_expeditions += 1
        total_crew_members += crew_members
        unique_years.add(year)

    if total_expeditions > 0:
        average_crew_members = round(total_crew_members / total_expeditions, 2)
    else:
        average_crew_members = 0.00

    report = (f'Total number of expeditions: {total_expeditions}\n'
              f'Total number of crew members: {total_crew_members}\n'
              f'Average number of crew members per expedition: {average_crew_members:.2f}\n'
              f'Total number of unique years: {len(unique_years)}')

    with open(output_file, 'w') as out_file:
        out_file.write(report)