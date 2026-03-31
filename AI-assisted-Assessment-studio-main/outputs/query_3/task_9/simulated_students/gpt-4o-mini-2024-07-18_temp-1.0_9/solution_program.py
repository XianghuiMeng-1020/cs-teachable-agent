def alien_signal_count(signal_logs):
    result = {}
    for planet, signals in signal_logs.items():
        freq_count = {}
        for signal in signals:
            if signal in freq_count:
                freq_count[signal] += 1
            else:
                freq_count[signal] = 1
        result[planet] = freq_count
    return result