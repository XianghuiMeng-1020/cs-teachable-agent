def generate_expedition_summary(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
        
        total_expeditions = 0
        total_crew = 0
        years = set()

        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 4:
                try:
                    exp_id = int(parts[0].strip())
                    captain_name = parts[1].strip()
                    year = int(parts[2].strip())
                    crew_members = int(parts[3].strip())

                    total_expeditions += 1
                    total_crew += crew_members
                    years.add(year)
                except ValueError:
                    with open(output_file, 'w') as out_f:
                        out_f.write(f"Error: Invalid data entry '{line.strip()}'\n")
                    return
            else:
                with open(output_file, 'w') as out_f:
                    out_f.write(f"Error: Partial or malformed data: '{line.strip()}'\n")
                return

        average_crew_per_expedition = total_crew / total_expeditions if total_expeditions > 0 else 0.0

        with open(output_file, 'w') as out_f:
            out_f.write(f"Total Expeditions: {total_expeditions}\n")
            out_f.write(f"Total Crew Members: {total_crew}\n")
            out_f.write(f"Average Crew per Expedition: {average_crew_per_expedition:.2f}\n")
            out_f.write(f"Unique Years: {len(years)}\n")

    except FileNotFoundError:
        with open(output_file, 'w') as out_f:
            out_f.write("Error: Input file not found.\n")    
    except Exception as e:
        with open(output_file, 'w') as out_f:
            out_f.write(f"Error: {str(e)}\n")