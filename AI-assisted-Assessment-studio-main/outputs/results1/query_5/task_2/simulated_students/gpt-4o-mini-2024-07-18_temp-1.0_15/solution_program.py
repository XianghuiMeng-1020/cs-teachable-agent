def demigod_tasks(filename):
    tasks_summary = {'mortal': (0, 0), 'divine': (0, 0)}
    for line in open(filename):
        line = line.strip()
        if not line:
            continue
        name, task_type, priority = line.split(',')
        priority = int(priority)
        if task_type in tasks_summary:
            count, total_priority = tasks_summary[task_type]
            count += 1
            total_priority += priority
            average_priority = total_priority // count
            tasks_summary[task_type] = (count, average_priority)
    return tasks_summary