def demigod_tasks(filename):
    tasks = {'mortal': (0, 0), 'divine': (0, 0)}
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():  # Ignore empty lines
                name, task_type, priority = line.strip().split(',')
                priority = int(priority)
                count, total_priority = tasks[task_type]
                tasks[task_type] = (count + 1, total_priority + priority)

    # Calculate average priorities
    for task_type in tasks:
        count, total_priority = tasks[task_type]
        if count > 0:
            average_priority = total_priority // count
        else:
            average_priority = 0
        tasks[task_type] = (count, average_priority)

    return tasks