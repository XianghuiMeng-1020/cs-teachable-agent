def extract_artifacts(file_path):
    artifacts = set()
    with open(file_path, 'r') as file:
        for line in file:
            items = line.strip().split(';')
            # Skip the first item which is the mythological figure
            artifacts.update(items[1:])
    sorted_artifacts = sorted(artifacts)
    with open('artifacts.txt', 'w') as output_file:
        for artifact in sorted_artifacts:
            output_file.write(artifact + '\n')