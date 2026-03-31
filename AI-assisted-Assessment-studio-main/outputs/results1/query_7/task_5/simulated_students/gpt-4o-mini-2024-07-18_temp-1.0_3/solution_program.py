def extract_artifacts(file_path):
    artifacts = set()
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(';')
            for artifact in parts[1:]:
                artifacts.add(artifact)
    sorted_artifacts = sorted(artifacts)
    output_path = 'artifacts.txt'
    with open(output_path, 'w') as output_file:
        for artifact in sorted_artifacts:
            output_file.write(f"{artifact}\n")