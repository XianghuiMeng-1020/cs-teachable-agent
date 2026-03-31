import os

def calculate_scores(input_file, output_file):
    # Initialize dictionary to store total scores for each player
    player_scores = {}
    
    # Read from the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()
        
        # Loop through each line to process player scores
        for line in lines:
            player_name, game_name, score = line.strip().split(',')
            score = int(score)
            
            if player_name not in player_scores:
                player_scores[player_name] = 0
            player_scores[player_name] += score

    # Sort players by name
    sorted_players = sorted(player_scores.items())

    # Write the results to the output file
    with open(output_file, 'w') as file:
        for player_name, total_score in sorted_players:
            file.write(f'{player_name},{total_score}\n')

# The solution function incorporates the use of variables to store and manipulate data (player_scores),
# loops to iterate over lines in the file, lists (along with dictionary) to store and sort the scores,
# and file handling with I/O operations to read from and write to files.