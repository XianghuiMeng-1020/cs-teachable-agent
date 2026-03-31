def count_danger_messages(logs):
    return sum(log.count('DANGER') for log in logs)