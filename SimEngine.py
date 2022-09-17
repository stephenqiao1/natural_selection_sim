import random

class Food():
    def __init__(self, x, y):
        self.food_score = 1
        self.position = (x, y)

class Blob():
    def __init__(self, speed, radius, sense, color, x_pos, y_pos):
        self.speed = speed
        self.size = radius
        self.sense = sense
        self.energy = 100
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos

    def replicate(self, speed, size, sense, color, x_pos, y_pos):
        self.population.append(Blob(speed, size, sense, color, x_pos, y_pos))

    def move(self):
        self.x_pos += self.speed
        self.y_pos += self.speed

class Population():
    def __init__(self):
        self.foods = []
        self.blobs = [Blob(10, 10, 10, (200, 200, 200), 10, 10)]

    def store_food(self, amount):  # creates a list of all the apples needed, each with different coordinates
        for x in range(amount):
            self.foods.append(Food(random.randint(0, 800), random.randint(0, 800)))\

        return self.foods

    def replicate_blobs(self, blob):  # adds a blob to the population
        self.blobs.append(blob)