class Spaceship:
    def __init__(self, name: str, max_speed: int):
        self.name = name
        self.max_speed = max_speed

    def book_trip(self, destination: str, distance: int) -> str:
        if distance <= 0:
            raise ValueError("Distance must be a positive integer.")
        try:
            time = distance / self.max_speed
            return f"Trip to {destination} will take {time} hours."
        except ZeroDivisionError:
            return "Cannot book trip: spaceship speed is zero."