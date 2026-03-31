class Spaceship:
    def __init__(self, name, max_speed):
        self.name = name
        self.max_speed = max_speed

    def book_trip(self, destination, distance):
        if distance <= 0:
            raise ValueError("Distance must be a positive integer.")
        try:
            time = distance / self.max_speed
            return f"Trip to {destination} will take {time} hours."
        except ZeroDivisionError:
            return "Cannot book trip: spaceship speed is zero."

# Example usage
if __name__ == "__main__":
    spaceship = Spaceship('Galactic Voyager', 5)
    print(spaceship.book_trip('Alpha Centauri', 20))  # Expected: "Trip to Alpha Centauri will take 4.0 hours."

    spaceship = Spaceship('Light Slug', 0)
    print(spaceship.book_trip('Proxima Centauri', 15))  # Expected: "Cannot book trip: spaceship speed is zero."

    spaceship = Spaceship('Cosmos Racer', 10)
    try:
        print(spaceship.book_trip('Sirius', 0))
    except ValueError as e:
        print(e)  # Expected: "Distance must be a positive integer."

    spaceship = Spaceship('Star Hopper', 10)
    try:
        print(spaceship.book_trip('Vega', -5))
    except ValueError as e:
        print(e)  # Expected: "Distance must be a positive integer."

    spaceship = Spaceship('Galaxy Cruiser', 100000)
    print(spaceship.book_trip('Andromeda', 1000000))  # Expected: "Trip to Andromeda will take 10.0 hours."