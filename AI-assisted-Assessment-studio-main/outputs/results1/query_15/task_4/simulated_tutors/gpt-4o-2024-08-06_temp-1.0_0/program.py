def count_danger_messages(logs):
    count = 0
    for log in logs:  # Loop through each log
        count += log.count("DANGER")  # Count occurrences of "DANGER" in each log string
    return count
