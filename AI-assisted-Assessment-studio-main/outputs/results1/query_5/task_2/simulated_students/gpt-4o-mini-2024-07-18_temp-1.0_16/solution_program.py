def demigod_tasks(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    task_summary = {'mortal': (0, 0), 'divine': (0, 0)}
    mortal_count, mortal_total_priority = 0, 0
    divine_count, divine_total_priority = 0, 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        name, task_type, priority = line.split(',')
        priority = int(priority)
        
        if task_type == 'mortal':
            mortal_count += 1
            mortal_total_priority += priority
        elif task_type == 'divine':
            divine_count += 1
            divine_total_priority += priority
    
    if mortal_count > 0:
        task_summary['mortal'] = (mortal_count, mortal_total_priority // mortal_count)
    if divine_count > 0:
        task_summary['divine'] = (divine_count, divine_total_priority // divine_count)
    
    return task_summary