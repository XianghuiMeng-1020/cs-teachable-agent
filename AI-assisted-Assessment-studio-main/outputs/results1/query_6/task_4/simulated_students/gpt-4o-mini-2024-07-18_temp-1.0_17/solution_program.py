class MythologyDatabase:
    def __init__(self):
        self.gods = []

    def add_god(self, name, domain, origin):
        self.gods.append({'name': name, 'domain': domain, 'origin': origin})

    def remove_god(self, name):
        self.gods = [god for god in self.gods if god['name'] != name]

    def search_god(self, name):
        for god in self.gods:
            if god['name'] == name:
                return f"{god['name']};{god['domain']};{god['origin']}"
        return "Not Found"

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            for god in self.gods:
                f.write(f"{god['name']};{god['domain']};{god['origin']}\n")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                self.gods = []
                for line in f:
                    name, domain, origin = line.strip().split(';')
                    self.add_god(name, domain, origin)
        except FileNotFoundError:
            self.gods = []
