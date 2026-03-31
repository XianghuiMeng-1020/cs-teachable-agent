def calculate_score(settlementsA, settlementsB, specialLocations):
    scoreA = 0
    scoreB = 0
    n = len(specialLocations)

    for i in range(n):
        if specialLocations[i] == 'S':
            # Check settlement A on the special tile position and its neighbors
            if settlementsA[i] == '1':
                scoreA += 1
            if i > 0 and settlementsA[i-1] == '1':
                scoreA += 1
            if i < n - 1 and settlementsA[i+1] == '1':
                scoreA += 1

            # Check settlement B on the special tile position and its neighbors
            if settlementsB[i] == '1':
                scoreB += 1
            if i > 0 and settlementsB[i-1] == '1':
                scoreB += 1
            if i < n - 1 and settlementsB[i+1] == '1':
                scoreB += 1

    if scoreA > scoreB:
        return 'A'
    elif scoreB > scoreA:
        return 'B'
    else:
        return 'Tie'