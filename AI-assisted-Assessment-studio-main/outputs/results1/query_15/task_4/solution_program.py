def count_danger_messages(logs):
    danger_count = 0
    for log in logs:
        index = 0
        while index != -1:
            index = log.find("DANGER", index)
            if index != -1:
                danger_count += 1
                index += len("DANGER")
    return danger_count
