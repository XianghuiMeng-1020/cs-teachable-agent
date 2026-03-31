def generate_ingredient_report():
    input_file = 'recipes.txt'
    output_file = 'ingredient_report.txt'
    ingredients_count = {}

    try:
        with open(input_file, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 2:
                    continue
                ingredients = parts[1].split(',')
                for ingredient in ingredients:
                    ingredient = ingredient.strip()
                    if ingredient:
                        if ingredient in ingredients_count:
                            ingredients_count[ingredient] += 1
                        else:
                            ingredients_count[ingredient] = 1

        ingredients_sorted = sorted(ingredients_count.items(), key=lambda x: x[1], reverse=True)

        with open(output_file, 'w') as file:
            for ingredient, count in ingredients_sorted:
                file.write(f"{ingredient}: {count}\n")

    except FileNotFoundError:
        open(output_file, 'w').close()