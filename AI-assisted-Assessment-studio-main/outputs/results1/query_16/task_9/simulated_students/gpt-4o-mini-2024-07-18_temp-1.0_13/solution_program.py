class Starship:
    def __init__(self, initial_time_travelled, velocity_factor):
        self.initial_time_travelled = initial_time_travelled
        self.velocity_factor = velocity_factor
        self.effective_time = 0.0

    def travel_through_wormhole(self, wormhole_intensity):
        self.effective_time = self.initial_time_travelled * wormhole_intensity * self.velocity_factor

    def get_effective_time(self):
        return f'{self.effective_time:.2f} years'

    def handle_exception_test(self):
        try:
            _ = 1 / 0
        except ZeroDivisionError:
            return 'Handled Exception: Division by zero.'