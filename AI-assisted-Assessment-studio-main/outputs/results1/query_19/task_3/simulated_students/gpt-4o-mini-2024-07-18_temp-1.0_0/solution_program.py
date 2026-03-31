def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        with open(output_file, 'w') as out_file:
            out_file.write("Error: Input file not found.")
        return
    except Exception as e:
        with open(output_file, 'w') as out_file:
            out_file.write(f"Error: {str(e)}")
        return

    total_expeditions = 0
    total_crew_members = 0
    unique_years = set()

    for line in lines:
        try:
            expedition_id, captain, year, crew_members = line.strip().split(',')
            expedition_id = int(expedition_id)
            year = int(year)
            crew_members = int(crew_members)

            total_expeditions += 1
            total_crew_members += crew_members
            unique_years.add(year)
        except ValueError:
            with open(output_file, 'w') as out_file:
                out_file.write("Error: Invalid data format in input file.")
            return

    if total_expeditions == 0:
        average_crew_members = 0.0
    else:
        average_crew_members = total_crew_members / total_expeditions

    with open(output_file, 'w') as out_file:
        out_file.write(f"Total expeditions: {total_expeditions}\n")
        out_file.write(f"Total crew members: {total_crew_members}\n")
        out_file.write(f"Average crew members per expedition: {average_crew_members:.2f}\n")
        out_file.write(f"Unique years: {len(unique_years)}\n")