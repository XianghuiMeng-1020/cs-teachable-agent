def determine_weather(readings, threshold):
    count = 0
    
    for reading in readings:
        if reading > threshold:
            count += 1
    
    if count > len(readings) / 2:
        return 'Stormy'
    else:
        return 'Calm'