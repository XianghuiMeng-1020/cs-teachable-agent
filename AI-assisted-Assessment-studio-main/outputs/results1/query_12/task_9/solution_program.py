def find_low_cal_recipes(threshold):
    low_cal_recipes = []
    with open('recipe_calories.txt', 'r') as file:
        for line in file:
            name, calories = line.strip().split(': ')
            if int(calories) <= threshold:
                low_cal_recipes.append(name)
    return low_cal_recipes