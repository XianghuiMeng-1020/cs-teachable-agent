def demigod_tasks(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    tasks_summary = {'mortal': [0, 0], 'divine': [0, 0]}  # [count, total_priority]

    for line in lines:
        line = line.strip()  # Remove leading and trailing whitespace
        if not line:  # Skip empty lines
            continue
        name, task_type, priority = line.split(',')
        priority = int(priority)

        if task_type in tasks_summary:
            tasks_summary[task_type][0] += 1  # Increment task count
            tasks_summary[task_type][1] += priority  # Add to total priority

    # Prepare the final summary with averages
    for task_type in tasks_summary:
        count, total_priority = tasks_summary[task_type]
        if count > 0:
            average_priority = total_priority // count  # Integer division
        else:
            average_priority = 0
        tasks_summary[task_type] = (count, average_priority)

    return tasks_summary