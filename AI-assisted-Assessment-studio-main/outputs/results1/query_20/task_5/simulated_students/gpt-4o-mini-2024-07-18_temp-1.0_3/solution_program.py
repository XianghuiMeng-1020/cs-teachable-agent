def calculate_score(settlementsA, settlementsB, specialLocations):
    def score(settlements):
        total_score = 0
        for i in range(len(settlements)):
            if settlements[i] == '1':
                if i > 0 and specialLocations[i - 1] == 'S':
                    total_score += 1
                if i < len(specialLocations) - 1 and specialLocations[i + 1] == 'S':
                    total_score += 1
        return total_score

    scoreA = score(settlementsA)
    scoreB = score(settlementsB)

    if scoreA > scoreB:
        return 'A'
    elif scoreB > scoreA:
        return 'B'
    else:
        return 'Tie'