class Lasergun:
    def __init__(self, total_energy: int):
        if total_energy <= 0:
            raise ValueError("Energy must be a positive integer.")
        self.total_energy = total_energy
        self.current_energy = total_energy

    def shoot(self):
        if self.current_energy >= 10:
            self.current_energy -= 10
            return "Pew! Pew!"
        else:
            return "Out of energy!"

    def reload(self):
        self.current_energy = self.total_energy

    def remaining_energy(self):
        return f"Remaining energy: {self.current_energy}"