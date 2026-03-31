def extract_artifacts(file_path):
    artifacts = set()
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(';')
            if len(parts) > 1:
                for artifact in parts[1:]:
                    artifacts.add(artifact)
    sorted_artifacts = sorted(artifacts)
    with open('artifacts.txt', 'w') as output_file:
        for artifact in sorted_artifacts:
            output_file.write(artifact + '\n')