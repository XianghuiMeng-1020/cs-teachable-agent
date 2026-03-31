class Spaceship:
    def __init__(self, name, max_speed):
        self.name = name
        self.max_speed = max_speed

    def book_trip(self, destination, distance):
        if distance <= 0:
            raise ValueError("Distance must be a positive integer.")
        try:
            time = distance / self.max_speed
        except ZeroDivisionError:
            return "Cannot book trip: spaceship speed is zero."
        return f"Trip to {destination} will take {time} hours."