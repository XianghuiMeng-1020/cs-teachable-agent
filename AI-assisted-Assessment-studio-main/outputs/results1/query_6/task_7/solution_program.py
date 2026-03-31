import os

class MythArchive:
    def __init__(self):
        self.storage_path = 'myth_archive'
        os.makedirs(self.storage_path, exist_ok=True)

    def add_tale(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
        tale_name = lines[0].strip()
        tale_content = ''.join(lines[1:]).strip()
        tale_file_path = os.path.join(self.storage_path, tale_name + '.txt')
        with open(tale_file_path, 'w') as f:
            f.write(tale_content)

    def get_tale(self, name):
        tale_file_path = os.path.join(self.storage_path, name + '.txt')
        if os.path.exists(tale_file_path):
            with open(tale_file_path, 'r') as f:
                return f.read().strip()
        return ''

    def remove_tale(self, name):
        tale_file_path = os.path.join(self.storage_path, name + '.txt')
        if os.path.exists(tale_file_path):
            os.remove(tale_file_path)

    def list_tales(self):
        return [file[:-4] for file in os.listdir(self.storage_path) if file.endswith('.txt')]