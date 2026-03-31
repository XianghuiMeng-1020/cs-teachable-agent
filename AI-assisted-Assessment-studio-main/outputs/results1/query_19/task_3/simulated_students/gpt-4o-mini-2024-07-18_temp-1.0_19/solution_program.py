def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        with open(output_file, 'w') as outfile:
            outfile.write("Error: Input file not found.\n")
        return
    except Exception as e:
        with open(output_file, 'w') as outfile:
            outfile.write(f"Error: {str(e)}\n")
        return

    total_expeditions = 0
    total_crew_members = 0
    years_set = set()

    for line in lines:
        try:
            parts = line.strip().split(',')
            expedition_id = int(parts[0])
            captain_name = parts[1].strip()
            year = int(parts[2])
            crew_members = int(parts[3])
            total_expeditions += 1
            total_crew_members += crew_members
            years_set.add(year)
        except (ValueError, IndexError) as e:
            with open(output_file, 'w') as outfile:
                outfile.write("Error: Data parsing error occurred.\n")
            return

    if total_expeditions == 0:
        average_crew_members = 0
    else:
        average_crew_members = total_crew_members / total_expeditions

    with open(output_file, 'w') as outfile:
        outfile.write(f"Total number of expeditions: {total_expeditions}\n")
        outfile.write(f"Total number of crew members: {total_crew_members}\n")
        outfile.write(f"Average number of crew members per expedition: {average_crew_members:.2f}\n")
        outfile.write(f"Total number of unique years: {len(years_set)}\n")