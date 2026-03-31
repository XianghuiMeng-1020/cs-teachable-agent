class Lasergun:
    def __init__(self, total_energy):
        if total_energy <= 0:
            raise ValueError("Invalid energy value.")
        self.total_energy = total_energy
        self.current_energy = total_energy

    def shoot(self):
        if self.current_energy < 10:
            return "Out of energy!"
        else:
            self.current_energy -= 10
            return "Pew! Pew!"

    def reload(self):
        self.current_energy = self.total_energy

    def remaining_energy(self):
        return f"Remaining energy: {self.current_energy}"

# Example usage:
# lasergun = Lasergun(100)
# print(lasergun.shoot())  # Expected: Pew! Pew!
# print(lasergun.remaining_energy())  # Expected: Remaining energy: 90
# lasergun.reload()
# print(lasergun.remaining_energy())  # Expected: Remaining energy: 100