def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            records = infile.readlines()
    except FileNotFoundError:
        with open(output_file, 'w') as outfile:
            outfile.write('Error: Input file not found.\n')
        return
    except Exception as e:
        with open(output_file, 'w') as outfile:
            outfile.write(f'Error: {str(e)}.\n')
        return
    
    total_expeditions = 0
    total_crew_members = 0
    years = set()

    for record in records:
        parts = record.strip().split(',')
        if len(parts) != 4:
            continue
        try:
            expedition_id = int(parts[0])
            captain_name = parts[1]
            year = int(parts[2])
            crew_members = int(parts[3])
        except ValueError:
            continue

        total_expeditions += 1
        total_crew_members += crew_members
        years.add(year)

    unique_years = len(years)
    average_crew_members = total_crew_members / total_expeditions if total_expeditions > 0 else 0.0

    with open(output_file, 'w') as outfile:
        outfile.write(f'Total Expeditions: {total_expeditions}\n')
        outfile.write(f'Total Crew Members: {total_crew_members}\n')
        outfile.write(f'Average Crew Members per Expedition: {average_crew_members:.2f}\n')
        outfile.write(f'Unique Years of Expeditions: {unique_years}\n')