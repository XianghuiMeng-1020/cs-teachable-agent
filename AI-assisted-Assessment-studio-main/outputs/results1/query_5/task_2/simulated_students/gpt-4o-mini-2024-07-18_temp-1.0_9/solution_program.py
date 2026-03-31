def demigod_tasks(filename):
    task_summary = {'mortal': (0, 0), 'divine': (0, 0)}
    mortal_count = 0
    mortal_priority_sum = 0
    divine_count = 0
    divine_priority_sum = 0

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            name, task_type, priority_str = line.split(',')
            priority = int(priority_str)

            if task_type == 'mortal':
                mortal_count += 1
                mortal_priority_sum += priority
            elif task_type == 'divine':
                divine_count += 1
                divine_priority_sum += priority

    if mortal_count > 0:
        mortal_average = mortal_priority_sum // mortal_count
    else:
        mortal_average = 0

    if divine_count > 0:
        divine_average = divine_priority_sum // divine_count
    else:
        divine_average = 0

    task_summary['mortal'] = (mortal_count, mortal_average)
    task_summary['divine'] = (divine_count, divine_average)

    return task_summary