def extract_artifacts(file_path):
    artifacts = set()
    with open(file_path, 'r') as file:
        for line in file:
            items = line.strip().split(';')
            if len(items) > 1:
                # Skip the first item which is the mythological figure
                artifacts.update(items[1:])
    sorted_artifacts = sorted(artifacts)
    with open('artifacts.txt', 'w') as outfile:
        for artifact in sorted_artifacts:
            outfile.write(artifact + '\n')