import os

def calculate_score(input_file):
    total_score = 0
    with open(input_file, 'r') as file:
        for line in file:
            roll = int(line.strip())
            if roll == 6:
                score = 0
            elif roll % 2 == 0:  # Even number
                score = roll * 2
            else:  # Odd number
                score = roll * 3
            total_score += score
    with open('score.txt', 'w') as file:
        file.write(f"{total_score}")

# The main execution does not need to be invoked explicitly here,
# as this code setup is for the function to be imported and tested separately.