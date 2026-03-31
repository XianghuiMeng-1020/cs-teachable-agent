def demigod_tasks(filename):
    tasks_summary = {'mortal': (0, 0), 'divine': (0, 0)}
    for task_line in open(filename):
        task_line = task_line.strip()
        if not task_line:
            continue
        name, task_type, priority = task_line.split(',')
        priority = int(priority)
        if task_type in tasks_summary:
            current_count, current_total_priority = tasks_summary[task_type]
            new_count = current_count + 1
            new_total_priority = current_total_priority + priority
            average_priority = new_total_priority // new_count
            tasks_summary[task_type] = (new_count, average_priority)
    return tasks_summary