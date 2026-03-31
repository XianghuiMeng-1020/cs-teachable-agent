import os

class MythArchive:
    def __init__(self):
        self.directory = 'myth_archive'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def add_tale(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                name = lines[0].strip()
                content = ''.join(lines[1:])
                with open(os.path.join(self.directory, name), 'w') as tale_file:
                    tale_file.write(content)

    def get_tale(self, name):
        try:
            with open(os.path.join(self.directory, name), 'r') as tale_file:
                return tale_file.read()
        except FileNotFoundError:
            return ''

    def remove_tale(self, name):
        try:
            os.remove(os.path.join(self.directory, name))
        except FileNotFoundError:
            pass

    def list_tales(self):
        return os.listdir(self.directory)