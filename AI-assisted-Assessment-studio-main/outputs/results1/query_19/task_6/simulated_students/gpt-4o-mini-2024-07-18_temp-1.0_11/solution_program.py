import os

def analyze_asteroid_reports(input_filename, output_filename):
    if not os.path.exists(input_filename):
        with open(output_filename, 'w') as file:
            file.write('No data available')
        return
    
    total_force = 0
    count = 0
    
    with open(input_filename, 'r') as file:
        for line in file:
            if line.strip():
                asteroid_id, impact_force = line.split(',')
                total_force += float(impact_force)
                count += 1
    
    with open(output_filename, 'w') as file:
        if count == 0:
            file.write('No data available')
        else:
            average_force = total_force / count
            file.write(f'average impact force: {average_force}')