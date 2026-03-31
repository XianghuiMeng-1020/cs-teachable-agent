def alien_signal_count(signal_logs):
    signal_count = {}
    for planet, signals in signal_logs.items():
        frequency = {}
        for signal in signals:
            if signal in frequency:
                frequency[signal] += 1
            else:
                frequency[signal] = 1
        signal_count[planet] = frequency
    return signal_count