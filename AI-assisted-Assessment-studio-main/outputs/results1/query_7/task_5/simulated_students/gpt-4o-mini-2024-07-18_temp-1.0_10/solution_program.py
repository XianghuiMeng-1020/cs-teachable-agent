def extract_artifacts(file_path):
    artifacts_set = set()
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(';')[1:]
            artifacts_set.update(parts)
    sorted_artifacts = sorted(artifacts_set)
    with open('artifacts.txt', 'w') as output_file:
        for artifact in sorted_artifacts:
            output_file.write(artifact + '\n')