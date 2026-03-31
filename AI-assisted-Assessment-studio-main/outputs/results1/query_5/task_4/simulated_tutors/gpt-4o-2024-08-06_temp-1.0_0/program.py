def get_strengthiest_beast(filename):
    # Initialize variables to track the strongest beast and its strength
    max_strength = -1
    strengthiest_beast = ""
    
    # Open the file in read mode
    with open(filename, 'r') as file:
        for line in file:
            # Strip whitespace and split each line into name and strength
            name, strength = line.strip().split(',')
            
            # Convert strength to an integer
            strength = int(strength)

            # Compare to find the highest strength beast
            if strength > max_strength:
                max_strength = strength
                strengthiest_beast = name
                
    return strengthiest_beast
