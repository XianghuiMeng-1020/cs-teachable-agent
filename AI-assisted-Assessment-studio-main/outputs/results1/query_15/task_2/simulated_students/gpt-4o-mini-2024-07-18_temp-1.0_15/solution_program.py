def determine_weather(readings, threshold):
    above_threshold_count = sum(1 for reading in readings if reading > threshold)
    if above_threshold_count > len(readings) / 2:
        return 'Stormy'
    else:
        return 'Calm'