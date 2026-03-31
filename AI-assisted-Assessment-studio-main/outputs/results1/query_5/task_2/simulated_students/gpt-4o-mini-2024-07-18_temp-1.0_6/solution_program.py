def demigod_tasks(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    tasks_summary = {'mortal': (0, 0), 'divine': (0, 0)}
    mortal_count = 0
    mortal_priority_sum = 0
    divine_count = 0
    divine_priority_sum = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        name, task_type, priority = line.split(',')
        priority = int(priority)

        if task_type == 'mortal':
            mortal_count += 1
            mortal_priority_sum += priority
        elif task_type == 'divine':
            divine_count += 1
            divine_priority_sum += priority

    # Calculate averages
    if mortal_count > 0:
        mortal_average = mortal_priority_sum // mortal_count
    else:
        mortal_average = 0

    if divine_count > 0:
        divine_average = divine_priority_sum // divine_count
    else:
        divine_average = 0

    tasks_summary['mortal'] = (mortal_count, mortal_average)
    tasks_summary['divine'] = (divine_count, divine_average)

    return tasks_summary