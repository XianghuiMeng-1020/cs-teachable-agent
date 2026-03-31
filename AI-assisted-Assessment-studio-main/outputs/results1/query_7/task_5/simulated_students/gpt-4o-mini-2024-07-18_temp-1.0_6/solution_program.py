def extract_artifacts(file_path):
    artifacts = set()
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(';')
            if len(parts) > 1:
                artifacts.update(parts[1:])
    sorted_artifacts = sorted(artifacts)
    with open('artifacts.txt', 'w') as out_file:
        for artifact in sorted_artifacts:
            out_file.write(artifact + '\n')