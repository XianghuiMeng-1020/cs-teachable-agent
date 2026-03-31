def demigod_tasks(filename):
    # Initialize a dictionary to hold tasks information
    tasks_summary = {'mortal': (0, 0), 'divine': (0, 0)}
    mortal_count = 0
    divine_count = 0
    mortal_priority_sum = 0
    divine_priority_sum = 0

    # Read the tasks from the file
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading and trailing whitespace
            if not line:  # Skip empty lines
                continue
            task_info = line.split(',')  # Split the line into components
            name, task_type, priority = task_info[0], task_info[1], int(task_info[2])

            if task_type == 'mortal':
                mortal_count += 1
                mortal_priority_sum += priority
            elif task_type == 'divine':
                divine_count += 1
                divine_priority_sum += priority

    # Calculate average priorities
    mortal_average = mortal_priority_sum // mortal_count if mortal_count > 0 else 0
    divine_average = divine_priority_sum // divine_count if divine_count > 0 else 0

    # Update the summary dictionary with counts and average priorities
    tasks_summary['mortal'] = (mortal_count, mortal_average)
    tasks_summary['divine'] = (divine_count, divine_average)

    return tasks_summary