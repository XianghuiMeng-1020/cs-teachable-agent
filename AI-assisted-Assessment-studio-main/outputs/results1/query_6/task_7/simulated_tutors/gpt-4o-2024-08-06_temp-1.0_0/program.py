import os

class MythArchive:
    def __init__(self):
        self.archive_path = 'myth_archive'
        os.makedirs(self.archive_path, exist_ok=True)

    def add_tale(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            tale_name = lines[0].strip()
            tale_content = ''.join(lines[1:]).strip()

        tale_file_path = os.path.join(self.archive_path, f'{tale_name}.txt')
        with open(tale_file_path, 'w') as tale_file:
            tale_file.write(tale_content)

    def get_tale(self, name):
        tale_file_path = os.path.join(self.archive_path, f'{name}.txt')
        try:
            with open(tale_file_path, 'r') as tale_file:
                return tale_file.read().strip()
        except FileNotFoundError:
            return ''

    def remove_tale(self, name):
        tale_file_path = os.path.join(self.archive_path, f'{name}.txt')
        try:
            os.remove(tale_file_path)
        except FileNotFoundError:
            pass

    def list_tales(self):
        return [os.path.splitext(file_name)[0] for file_name in os.listdir(self.archive_path)]