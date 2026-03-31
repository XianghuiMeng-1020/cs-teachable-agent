class MythologyDatabase:
    def __init__(self):
        self.gods = []

    def add_god(self, name, domain, origin):
        self.gods.append(f"{name};{domain};{origin}")

    def remove_god(self, name):
        self.gods = [god for god in self.gods if not god.startswith(name + ';')]

    def search_god(self, name):
        for god in self.gods:
            if god.startswith(name + ';'):
                return god
        return "Not Found"

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for god in self.gods:
                file.write(god + '\n')

    def load_from_file(self, filename):
        self.gods = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    self.gods.append(line.strip())
        except FileNotFoundError:
            pass
