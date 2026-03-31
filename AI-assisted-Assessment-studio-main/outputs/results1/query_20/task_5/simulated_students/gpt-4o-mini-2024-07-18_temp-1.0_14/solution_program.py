def calculate_score(settlementsA, settlementsB, specialLocations):
    scoreA = 0
    scoreB = 0
    length = len(settlementsA)
    
    for i in range(length):
        if specialLocations[i] == 'S':
            if i > 0 and settlementsA[i-1] == '1':
                scoreA += 1
            if i < length - 1 and settlementsA[i+1] == '1':
                scoreA += 1
            if i > 0 and settlementsB[i-1] == '1':
                scoreB += 1
            if i < length - 1 and settlementsB[i+1] == '1':
                scoreB += 1
    
    if scoreA > scoreB:
        return 'A'
    elif scoreB > scoreA:
        return 'B'
    else:
        return 'Tie'