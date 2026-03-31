def alien_signal_count(signal_logs):
    signal_frequency = {}
    for planet, signals in signal_logs.items():
        frequency = {}
        for signal in signals:
            if signal in frequency:
                frequency[signal] += 1
            else:
                frequency[signal] = 1
        signal_frequency[planet] = frequency
    return signal_frequency