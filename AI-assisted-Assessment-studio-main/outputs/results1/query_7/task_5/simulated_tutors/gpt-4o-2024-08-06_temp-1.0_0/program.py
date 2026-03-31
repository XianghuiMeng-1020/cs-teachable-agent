def extract_artifacts(file_path):
    # Use a set to store unique artifacts
    artifacts_set = set()
    
    # Open the input file and read its contents
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by semicolon and ignore the first item (figure's name)
            items = line.strip().split(';')[1:]
            # Add each artifact to the set
            artifacts_set.update(items)
    
    # Convert the set to a sorted list
    sorted_artifacts = sorted(artifacts_set)
    
    # Write the sorted artifacts to 'artifacts.txt' file
    with open('artifacts.txt', 'w') as file:
        for artifact in sorted_artifacts:
            file.write(artifact + '\n')