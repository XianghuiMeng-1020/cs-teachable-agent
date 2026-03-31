def determine_weather(readings, threshold):
    count_above_threshold = 0
    total_readings = len(readings)
    
    for reading in readings:
        if reading > threshold:
            count_above_threshold += 1
    
    if count_above_threshold > total_readings / 2:
        return "Stormy"
    else:
        return "Calm"