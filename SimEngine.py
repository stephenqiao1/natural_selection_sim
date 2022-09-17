import random

class Food():
    def __init__(self):
        self.food_storage = []

    def store_food(self, amount):  # creates a list of all the apples needed, each with different coordinates
        for x in range(amount):
            self.food_storage.append((random.randint(0, 800), random.randint(0,800)))


class Blob():
    def __init__(self, speed, size, sense, color):
        self.speed = speed
        self.size = size
        self.sense = sense
        self.energy = 100
        self.color = color