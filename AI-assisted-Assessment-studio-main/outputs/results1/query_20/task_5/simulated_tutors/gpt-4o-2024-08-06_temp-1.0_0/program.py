def calculate_score(settlementsA, settlementsB, specialLocations):
    # Calculate the score for each player based on adjacency to special locations
    def score(settlements):
        score = 0
        for i in range(len(specialLocations)):
            if specialLocations[i] == 'S':
                if i > 0 and settlements[i-1] == '1':
                    score += 1
                if i < len(specialLocations) - 1 and settlements[i+1] == '1':
                    score += 1
        return score

    # Calculate scores for Player A and Player B
    scoreA = score(settlementsA)
    scoreB = score(settlementsB)

    # Compare scores and return the result
    if scoreA > scoreB:
        return 'A'
    elif scoreB > scoreA:
        return 'B'
    else:
        return 'Tie'