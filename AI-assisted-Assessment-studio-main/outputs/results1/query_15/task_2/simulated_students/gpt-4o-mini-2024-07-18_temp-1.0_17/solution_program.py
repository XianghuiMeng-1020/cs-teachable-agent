def determine_weather(readings, threshold):
    above_threshold_count = sum(1 for reading in readings if reading > threshold)
    total_readings = len(readings)
    if above_threshold_count > total_readings / 2:
        return 'Stormy'
    else:
        return 'Calm'