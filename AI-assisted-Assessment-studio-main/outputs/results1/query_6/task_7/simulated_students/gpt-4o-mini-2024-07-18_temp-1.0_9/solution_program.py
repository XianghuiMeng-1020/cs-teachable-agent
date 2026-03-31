import os

class MythArchive:
    def __init__(self):
        self.directory = 'myth_archive'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def add_tale(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if lines:
                tale_name = lines[0].strip()
                tale_content = ''.join(lines[1:])
                with open(os.path.join(self.directory, tale_name + '.txt'), 'w', encoding='utf-8') as tale_file:
                    tale_file.write(tale_content)

    def get_tale(self, name):
        tale_file_path = os.path.join(self.directory, name + '.txt')
        if os.path.exists(tale_file_path):
            with open(tale_file_path, 'r', encoding='utf-8') as tale_file:
                return tale_file.read()
        return ''

    def remove_tale(self, name):
        tale_file_path = os.path.join(self.directory, name + '.txt')
        if os.path.exists(tale_file_path):
            os.remove(tale_file_path)

    def list_tales(self):
        return [file[:-4] for file in os.listdir(self.directory) if file.endswith('.txt')]