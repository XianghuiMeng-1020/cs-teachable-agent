def alien_signal_count(signal_logs):
    result = {}
    for planet, signals in signal_logs.items():
        signal_count = {}
        for signal in signals:
            if signal in signal_count:
                signal_count[signal] += 1
            else:
                signal_count[signal] = 1
        result[planet] = signal_count
    return result
