def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()

        total_expeditions = 0
        total_crew_members = 0
        years = set()

        for line in lines:
            total_expeditions += 1
            parts = line.strip().split(',')
            if len(parts) != 4:
                continue
            try:
                expedition_id = int(parts[0])
                captain_name = parts[1].strip()
                year = int(parts[2])
                crew_members = int(parts[3])
                total_crew_members += crew_members
                years.add(year)
            except ValueError:
                continue

        if total_expeditions > 0:
            average_crew_members = total_crew_members / total_expeditions
        else:
            average_crew_members = 0

        with open(output_file, 'w') as out_file:
            out_file.write(f'Total number of expeditions: {total_expeditions}\n')
            out_file.write(f'Total number of crew members: {total_crew_members}\n')
            out_file.write(f'Average number of crew members per expedition: {average_crew_members:.2f}\n')
            out_file.write(f'Total number of unique years: {len(years)}\n')

    except FileNotFoundError:
        with open(output_file, 'w') as out_file:
            out_file.write('Error: Input file not found.\n')
    except Exception as e:
        with open(output_file, 'w') as out_file:
            out_file.write(f'An error occurred: {str(e)}\n')