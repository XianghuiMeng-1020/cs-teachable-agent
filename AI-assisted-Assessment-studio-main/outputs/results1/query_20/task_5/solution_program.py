def calculate_score(settlementsA, settlementsB, specialLocations):
    scoreA = 0
    scoreB = 0
    for i in range(len(specialLocations)):
        if specialLocations[i] == 'S':
            if i > 0:
                if settlementsA[i - 1] == '1':
                    scoreA += 1
                if settlementsB[i - 1] == '1':
                    scoreB += 1
            if i < len(specialLocations) - 1:
                if settlementsA[i + 1] == '1':
                    scoreA += 1
                if settlementsB[i + 1] == '1':
                    scoreB += 1
    if scoreA > scoreB:
        return "A"
    elif scoreB > scoreA:
        return "B"
    else:
        return "Tie"