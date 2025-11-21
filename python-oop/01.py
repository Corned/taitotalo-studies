class Car:
    def __init__(self, brand, color, speed):
        self.brand = brand
        self.color = color
        self.speed = speed
        self.info = f"{self.brand}\nColor:{self.color}\nSpeed:{self.speed}"


audi = Car("Audi", "Red", 200)
print(audi.info)
