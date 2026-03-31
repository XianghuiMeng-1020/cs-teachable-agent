def demigod_tasks(filename):
    # Initialize a dictionary to keep track of the number of tasks and sum of priority for each type
    task_summary = {
        'mortal': {'count': 0, 'priority_sum': 0},
        'divine': {'count': 0, 'priority_sum': 0}
    }

    # Open and read the file
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            # Ignore empty lines
            if not line:
                continue

            # Split the line into name, type, and priority
            name, type_of_task, priority_str = line.split(',')
            priority = int(priority_str)

            # Use selection statements to decide which type to process
            if type_of_task in task_summary:
                task_summary[type_of_task]['count'] += 1
                task_summary[type_of_task]['priority_sum'] += priority

    # Prepare the result dictionary
    result = {}
    for task_type, data in task_summary.items():
        count = data['count']
        priority_sum = data['priority_sum']
        average_priority = priority_sum // count if count != 0 else 0
        result[task_type] = (count, average_priority)

    return result

# The program makes use of Variables, Arithmetic Operators, Selection Statements (if/else), and File Handling and I/O.