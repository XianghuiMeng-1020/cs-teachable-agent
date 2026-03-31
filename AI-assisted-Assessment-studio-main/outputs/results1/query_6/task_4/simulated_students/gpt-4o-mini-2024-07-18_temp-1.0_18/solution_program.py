class MythologyDatabase:
    def __init__(self):
        self.database = []

    def add_god(self, name, domain, origin):
        self.database.append({'name': name, 'domain': domain, 'origin': origin})

    def remove_god(self, name):
        self.database = [god for god in self.database if god['name'] != name]

    def search_god(self, name):
        for god in self.database:
            if god['name'] == name:
                return f"{god['name']};{god['domain']};{god['origin']}"
        return "Not Found"

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for god in self.database:
                file.write(f"{god['name']};{god['domain']};{god['origin']}\n")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.database = []
                for line in file:
                    name, domain, origin = line.strip().split(';')
                    self.add_god(name, domain, origin)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading file: {e}")