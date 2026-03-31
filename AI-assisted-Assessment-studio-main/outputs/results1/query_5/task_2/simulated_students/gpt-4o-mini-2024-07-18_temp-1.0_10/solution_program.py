def demigod_tasks(filename):
    task_summary = {'mortal': (0, 0), 'divine': (0, 0)}  # Initialize dictionary with (count, total_priority)
    for line in open(filename):
        line = line.strip()  # Remove leading/trailing whitespace 
        if line:
            name, task_type, priority = line.split(',')
            priority = int(priority)  # Convert priority to integer
            if task_type in task_summary:
                count, total_priority = task_summary[task_type]
                count += 1
                total_priority += priority
                task_summary[task_type] = (count, total_priority)

    # Calculate average priority
    for task_type in task_summary:
        count, total_priority = task_summary[task_type]
        if count > 0:
            average_priority = total_priority // count  # Integer division
        else:
            average_priority = 0
        task_summary[task_type] = (count, average_priority)

    return task_summary