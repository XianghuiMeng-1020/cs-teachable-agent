def find_winner(filename):
    # Read the race results from the file
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Initialize variables to hold the winner's name and time
    winner_name = None
    fastest_time = float('inf')

    # Process each line of the file
    for line in lines:
        # Strip any whitespace and split the line by comma
        parts = line.strip().split(',')
        name = parts[0]
        time = int(parts[1])
        
        # Check if this creature has the fastest time
        if time < fastest_time:
            fastest_time = time
            winner_name = name

    return winner_name
