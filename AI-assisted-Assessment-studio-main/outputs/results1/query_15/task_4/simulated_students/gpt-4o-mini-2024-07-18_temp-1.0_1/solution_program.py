def count_danger_messages(logs):
    count = 0
    for log in logs:
        count += log.count('DANGER')
    return count