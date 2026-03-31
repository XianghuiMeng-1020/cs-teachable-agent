def alien_signal_count(signal_logs):
    result = {}
    for planet, signals in signal_logs.items():
        frequency = {}
        for signal in signals:
            if signal in frequency:
                frequency[signal] += 1
            else:
                frequency[signal] = 1
        result[planet] = frequency
    return result