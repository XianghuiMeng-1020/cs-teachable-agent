class Lasergun:
    def __init__(self, total_energy):
        if total_energy <= 0:
            raise ValueError("Total energy must be a positive integer.")
        self.total_energy = total_energy
        self.remaining_energy_level = total_energy

    def shoot(self):
        if self.remaining_energy_level < 10:
            return "Out of energy!"
        self.remaining_energy_level -= 10
        return "Pew! Pew!"

    def reload(self):
        self.remaining_energy_level = self.total_energy

    def remaining_energy(self):
        return f"Remaining energy: {self.remaining_energy_level}"