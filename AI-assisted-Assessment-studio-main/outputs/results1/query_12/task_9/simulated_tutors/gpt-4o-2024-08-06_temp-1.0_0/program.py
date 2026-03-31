def find_low_cal_recipes(threshold):
    low_cal_recipes = []
    try:
        with open('recipe_calories.txt', 'r') as file:
            for line in file:
                if line.strip():  # Ensure line is not empty
                    # Split line into recipe name and calorie count
                    recipe, calories_str = line.split(':')
                    recipe = recipe.strip()
                    calories = int(calories_str.strip())

                    # Check if the calories are below the threshold
                    if calories <= threshold:
                        low_cal_recipes.append(recipe)
    except FileNotFoundError:
        print("The file recipe_calories.txt was not found.")
    return low_cal_recipes

# Include this main section for testing the function
if __name__ == "__main__":
    # Example test
    print(find_low_cal_recipes(250))
    # Add more tests if needed