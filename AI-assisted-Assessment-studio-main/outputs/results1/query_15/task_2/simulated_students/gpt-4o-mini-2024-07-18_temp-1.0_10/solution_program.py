def determine_weather(readings, threshold):
    stormy_count = sum(1 for reading in readings if reading > threshold)
    total_count = len(readings)
    if stormy_count > total_count / 2:
        return 'Stormy'
    else:
        return 'Calm'