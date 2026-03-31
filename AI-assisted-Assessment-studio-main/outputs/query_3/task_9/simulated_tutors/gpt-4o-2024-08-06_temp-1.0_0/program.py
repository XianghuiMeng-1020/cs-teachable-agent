def alien_signal_count(signal_logs):
    # Initialize an empty dictionary to store the result
    signal_count_by_planet = {}
    
    # Iterate over each planet and its log of signals
    for planet, signals in signal_logs.items():
        # Initialize an empty dictionary for counting signals for this planet
        signal_counts = {}
        
        # Iterate over each signal and count frequencies
        for signal in signals:
            if signal in signal_counts:
                signal_counts[signal] += 1
            else:
                signal_counts[signal] = 1
        
        # Assign the count dictionary to the corresponding planet in the result
        signal_count_by_planet[planet] = signal_counts
    
    return signal_count_by_planet