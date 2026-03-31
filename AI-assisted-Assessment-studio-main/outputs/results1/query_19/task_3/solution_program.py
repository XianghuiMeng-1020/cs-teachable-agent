def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()

        total_expeditions = 0
        total_crew = 0
        years = set()

        for line in lines:
            try:
                expedition_id, captain, year, crew = line.strip().split(',')
                total_expeditions += 1
                total_crew += int(crew)
                years.add(int(year))
            except ValueError:
                with open(output_file, 'w') as out:
                    out.write('Error: Invalid data format')
                return

        average_crew = round(total_crew / total_expeditions, 2) if total_expeditions else 0.00

        with open(output_file, 'w') as out:
            out.write(f"Total Expeditions: {total_expeditions}\n")
            out.write(f"Total Crew Members: {total_crew}\n")
            out.write(f"Average Crew per Expedition: {average_crew:.2f}\n")
            out.write(f"Unique Years: {len(years)}")
    except FileNotFoundError:
        with open(output_file, 'w') as out:
            out.write('Error: Input file not found')