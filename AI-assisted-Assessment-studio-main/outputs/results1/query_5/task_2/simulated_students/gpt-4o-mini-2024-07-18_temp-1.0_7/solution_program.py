def demigod_tasks(filename):
    # Initialize a dictionary to hold the task statistics
    tasks_summary = {'mortal': (0, 0), 'divine': (0, 0)}
    
    # Opens the tasks file for reading
    with open(filename, 'r') as file:
        total_mortal_priority = 0
        total_divine_priority = 0
        mortal_count = 0
        divine_count = 0
        
        # Read each line in the file
        for line in file:
            line = line.strip()  # Remove whitespace
            if line:  # Check if the line is not empty
                name, type_, priority = line.split(',')  # Split the line by commas
                priority = int(priority)  # Convert priority to an integer
                
                # Aggregate data based on task type
                if type_ == 'mortal':
                    mortal_count += 1
                    total_mortal_priority += priority
                elif type_ == 'divine':
                    divine_count += 1
                    total_divine_priority += priority

        # Calculate average priorities, rounding down
        average_mortal_priority = total_mortal_priority // mortal_count if mortal_count > 0 else 0
        average_divine_priority = total_divine_priority // divine_count if divine_count > 0 else 0
        
        # Update the task summary dictionary
        tasks_summary['mortal'] = (mortal_count, average_mortal_priority)
        tasks_summary['divine'] = (divine_count, average_divine_priority)
        
    return tasks_summary