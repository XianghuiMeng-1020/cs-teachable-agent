def demigod_tasks(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    tasks = {'mortal': [], 'divine': []}

    for line in lines:
        line = line.strip()
        if line:  # Ignore empty lines
            name, task_type, priority = line.split(',')
            priority = int(priority)
            if task_type in tasks:
                tasks[task_type].append(priority)

    result = {}
    for task_type, priority_list in tasks.items():
        if priority_list:
            total_tasks = len(priority_list)
            avg_priority = sum(priority_list) // total_tasks
            result[task_type] = (total_tasks, avg_priority)
        else:
            result[task_type] = (0, 0)

    return result