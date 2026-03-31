def determine_weather(readings, threshold):
    stormy_count = sum(1 for reading in readings if reading > threshold)
    if stormy_count > len(readings) / 2:
        return 'Stormy'
    return 'Calm'