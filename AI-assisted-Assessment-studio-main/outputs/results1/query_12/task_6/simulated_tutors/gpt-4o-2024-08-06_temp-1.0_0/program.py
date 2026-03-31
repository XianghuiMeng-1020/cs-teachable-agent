def organize_recipes(input_file):
    # Open the three output files in write mode
    with open('favorite_recipes.txt', 'w') as fav_file,
         open('to_try_recipes.txt', 'w') as try_file,
         open('disliked_recipes.txt', 'w') as dislike_file,
         open(input_file, 'r') as infile:
        
        for line in infile:
            recipe_name = line.strip()  # Read each recipe name and strip whitespace
            while True:
                user_input = input(f"How do you categorize '{recipe_name}'? (Favorite, To Try, Disliked): ").strip()
                if user_input in {'Favorite', 'To Try', 'Disliked'}:
                    break
                print("Invalid input. Please enter 'Favorite', 'To Try', or 'Disliked'.")
            
            # Write to the correct file based on user choice
            if user_input == 'Favorite':
                fav_file.write(recipe_name + '\n')
            elif user_input == 'To Try':
                try_file.write(recipe_name + '\n')
            elif user_input == 'Disliked':
                dislike_file.write(recipe_name + '\n')
