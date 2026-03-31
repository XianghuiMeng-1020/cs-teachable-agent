def demigod_tasks(filename):
    tasks_summary = {'mortal': (0, 0), 'divine': (0, 0)}
    total_mortal_priority = 0
    total_divine_priority = 0

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                name, task_type, priority = line.split(',')
                priority = int(priority)

                if task_type in tasks_summary:
                    count, total_priority = tasks_summary[task_type]
                    count += 1
                    total_priority += priority
                    tasks_summary[task_type] = (count, total_priority)

    for task_type in tasks_summary:
        count, total_priority = tasks_summary[task_type]
        if count > 0:
            average_priority = total_priority // count
        else:
            average_priority = 0
        tasks_summary[task_type] = (count, average_priority)

    return tasks_summary