def parse_ingredient_list(ingredient_str):
    # Initialize an empty dictionary to store the parsed ingredients
    ingredients = {}
    
    # Split the input string by semicolons to process each ingredient
    ingredient_list = ingredient_str.split(';')
    
    # Iterate over each ingredient in the list
    for ingredient in ingredient_list:
        # Split the ingredient details and strip spaces
        name, quantity, unit = [x.strip() for x in ingredient.split(',')]
        
        # Add the ingredient to the dictionary
        ingredients[name] = {'quantity': quantity, 'unit': unit}
    
    return ingredients

# Example usage
example_input = "flour,200,grams; sugar,100,grams; eggs,3,units"
print(parse_ingredient_list(example_input))
# Should output:
# {
#     'flour': {'quantity': '200', 'unit': 'grams'},
#     'sugar': {'quantity': '100', 'unit': 'grams'},
#     'eggs': {'quantity': '3', 'unit': 'units'}
# }