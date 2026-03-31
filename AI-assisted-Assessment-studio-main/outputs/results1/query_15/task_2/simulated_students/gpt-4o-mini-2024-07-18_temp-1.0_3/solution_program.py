def determine_weather(readings, threshold):
    count_above_threshold = sum(1 for reading in readings if reading > threshold)
    if count_above_threshold > len(readings) / 2:
        return 'Stormy'
    else:
        return 'Calm'