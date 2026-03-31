def calculate_score(settlementsA, settlementsB, specialLocations):
    def get_score(settlements):
        score = 0
        for i in range(len(specialLocations)):
            if specialLocations[i] == 'S':
                if i > 0 and settlements[i - 1] == '1':
                    score += 1
                if i < len(settlements) - 1 and settlements[i + 1] == '1':
                    score += 1
        return score

    scoreA = get_score(settlementsA)
    scoreB = get_score(settlementsB)

    if scoreA > scoreB:
        return 'A'
    elif scoreB > scoreA:
        return 'B'
    else:
        return 'Tie'