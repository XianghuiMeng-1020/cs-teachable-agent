def demigod_tasks(filename):
    tasks_summary = {'mortal': (0, 0), 'divine': (0, 0)}
    total_counts = {'mortal': 0, 'divine': 0}
    total_priorities = {'mortal': 0, 'divine': 0}

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(',')
                if len(parts) == 3:
                    name, task_type, priority_str = parts
                    priority = int(priority_str)
                    if task_type in total_counts:
                        total_counts[task_type] += 1
                        total_priorities[task_type] += priority

    for task_type in tasks_summary.keys():
        if total_counts[task_type] > 0:
            average_priority = total_priorities[task_type] // total_counts[task_type]
            tasks_summary[task_type] = (total_counts[task_type], average_priority)

    return tasks_summary