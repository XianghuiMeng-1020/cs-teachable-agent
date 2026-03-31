def count_danger_messages(logs):
    total_count = 0
    for log in logs:
        total_count += log.count('DANGER')
    return total_count