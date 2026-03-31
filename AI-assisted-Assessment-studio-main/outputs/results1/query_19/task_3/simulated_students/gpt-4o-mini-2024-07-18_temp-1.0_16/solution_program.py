def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            records = f.readlines()

        total_expeditions = len(records)
        total_crew_members = 0
        unique_years = set()

        for record in records:
            try:
                parts = record.strip().split(',')
                expedition_id = int(parts[0])
                captain_name = parts[1].strip()
                year = int(parts[2])
                crew_members = int(parts[3])
                total_crew_members += crew_members
                unique_years.add(year)
            except (ValueError, IndexError):
                continue  # Skip bad records

        average_crew_members = total_crew_members / total_expeditions if total_expeditions > 0 else 0
        average_crew_members = round(average_crew_members, 2)
        total_unique_years = len(unique_years)

        with open(output_file, 'w') as out:
            out.write(f'Total number of expeditions: {total_expeditions}\n')
            out.write(f'Total number of crew members: {total_crew_members}\n')
            out.write(f'Average number of crew members per expedition: {average_crew_members}\n')
            out.write(f'Total number of unique years: {total_unique_years}\n')

    except FileNotFoundError:
        with open(output_file, 'w') as out:
            out.write('Error: Input file not found.\n')
    except Exception as e:
        with open(output_file, 'w') as out:
            out.write(f'An unexpected error occurred: {str(e)}\n')