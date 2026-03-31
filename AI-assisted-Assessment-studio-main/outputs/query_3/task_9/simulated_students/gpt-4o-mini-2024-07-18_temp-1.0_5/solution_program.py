def alien_signal_count(signal_logs):
    result = {}
    for planet, signals in signal_logs.items():
        frequency = {}
        for signal in signals:
            frequency[signal] = frequency.get(signal, 0) + 1
        result[planet] = frequency
    return result