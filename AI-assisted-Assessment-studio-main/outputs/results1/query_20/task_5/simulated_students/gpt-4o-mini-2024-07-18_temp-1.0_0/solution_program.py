def calculate_score(settlementsA, settlementsB, specialLocations):
    def calculate_player_score(settlements, specialLocations):
        score = 0
        for i in range(len(settlements)):
            if settlements[i] == '1':
                if i > 0 and specialLocations[i - 1] == 'S':
                    score += 1
                if i < len(specialLocations) - 1 and specialLocations[i + 1] == 'S':
                    score += 1
        return score

    scoreA = calculate_player_score(settlementsA, specialLocations)
    scoreB = calculate_player_score(settlementsB, specialLocations)

    if scoreA > scoreB:
        return 'A'
    elif scoreB > scoreA:
        return 'B'
    else:
        return 'Tie'