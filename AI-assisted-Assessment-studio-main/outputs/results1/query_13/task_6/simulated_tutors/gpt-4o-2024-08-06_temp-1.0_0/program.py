def process_ingredient_usage(file_path):
    ingredient_usage = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # Strip any whitespace and split only once
                ingredient, usage = line.strip().split(':', 1)
                
                # If usage is not numeric, this will raise ValueError
                usage = int(usage)
                
                # Collect the ingredient usage
                if ingredient in ingredient_usage:
                    ingredient_usage[ingredient] += usage
                else:
                    ingredient_usage[ingredient] = usage
            except ValueError:
                # If the line was not correctly formatted, simply continue
                continue
            except IndexError:
                # In case split fails
                continue
    
    return ingredient_usage  

# Example usage:
# result = process_ingredient_usage('path_to_your_file.txt')
# print(result)