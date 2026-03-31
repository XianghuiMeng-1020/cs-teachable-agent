class MythologyDatabase:
    def __init__(self):
        self.database = {}

    def add_god(self, name, domain, origin):
        self.database[name] = {'domain': domain, 'origin': origin}

    def remove_god(self, name):
        if name in self.database:
            del self.database[name]

    def search_god(self, name):
        if name in self.database:
            god = self.database[name]
            return f"{name};{god['domain']};{god['origin']}"
        return "Not Found"

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for name, info in self.database.items():
                file.write(f"{name};{info['domain']};{info['origin']}\n")

    def load_from_file(self, filename):
        self.database.clear()
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        name, domain, origin = line.split(';')
                        self.database[name] = {'domain': domain, 'origin': origin}
        except FileNotFoundError:
            pass