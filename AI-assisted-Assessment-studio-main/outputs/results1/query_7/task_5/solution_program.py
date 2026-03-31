def extract_artifacts(file_path):
    with open(file_path, 'r') as file:
        artifact_set = set()
        for line in file:
            parts = line.strip().split(';')
            artifacts = parts[1:]
            artifact_set.update(artifacts)

    sorted_artifacts = sorted(artifact_set)

    with open('artifacts.txt', 'w') as file:
        for artifact in sorted_artifacts:
            file.write(f"{artifact}\n")