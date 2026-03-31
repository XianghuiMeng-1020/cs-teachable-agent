def demigod_tasks(filename):
    task_summary = {'mortal': (0, 0), 'divine': (0, 0)}
    tasks = {'mortal': [], 'divine': []}

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # ignoring empty lines
                name, type_task, priority = line.split(',')
                priority = int(priority)
                if type_task in tasks:
                    tasks[type_task].append(priority)

    for type_task, priorities in tasks.items():
        total_tasks = len(priorities)
        if total_tasks == 0:
            avg_priority = 0
        else:
            avg_priority = sum(priorities) // total_tasks  # integer division for average
        task_summary[type_task] = (total_tasks, avg_priority)

    return task_summary
