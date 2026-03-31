def count_danger_messages(logs):
    total_danger_count = 0
    for log in logs:
        total_danger_count += log.count('DANGER')
    return total_danger_count