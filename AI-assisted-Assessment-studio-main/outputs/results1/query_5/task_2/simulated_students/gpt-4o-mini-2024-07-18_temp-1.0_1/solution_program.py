def demigod_tasks(filename):
    with open(filename, 'r') as file:
        mortal_count = 0
        mortal_priority_sum = 0
        divine_count = 0
        divine_priority_sum = 0

        for line in file:
            line = line.strip()
            if line:
                name, task_type, priority = line.split(',')
                priority = int(priority)
                if task_type == 'mortal':
                    mortal_count += 1
                    mortal_priority_sum += priority
                elif task_type == 'divine':
                    divine_count += 1
                    divine_priority_sum += priority

    mortal_avg = mortal_priority_sum // mortal_count if mortal_count > 0 else 0
    divine_avg = divine_priority_sum // divine_count if divine_count > 0 else 0

    return {
        'mortal': (mortal_count, mortal_avg),
        'divine': (divine_count, divine_avg)
    }