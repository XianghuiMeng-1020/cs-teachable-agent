def calculate_score(settlementsA, settlementsB, specialLocations):
    def score_player(settlements):
        score = 0
        for i in range(len(settlements)):
            if settlements[i] == '1':
                if i > 0 and specialLocations[i - 1] == 'S':
                    score += 1
                if i < len(specialLocations) - 1 and specialLocations[i + 1] == 'S':
                    score += 1
        return score

    scoreA = score_player(settlementsA)
    scoreB = score_player(settlementsB)

    if scoreA > scoreB:
        return 'A'
    elif scoreB > scoreA:
        return 'B'
    else:
        return 'Tie'