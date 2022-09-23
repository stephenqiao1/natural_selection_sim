import random

class Food():
    def __init__(self, x, y):
        self.food_score = 1
        self.radius = 5
        self.x_pos = x
        self.y_pos = y

class Blob():
    def __init__(self, speed, radius, sense, color, x_pos, y_pos):
        self.speed = speed
        self.size = radius
        self.sense = sense
        self.food_eaten = 0
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_dir = True  # True if it is moving in the right direction, otherwise False if going left
        self.y_dir = True  # True if it is moving in the downwards direction, otherwise False if going up

    def move_in_space(self):
        # x-direction
        if self.x_dir:
            self.x_pos += self.speed
        elif not self.x_dir:
            self.x_pos += -1 * self.speed
        if self.x_pos >= 800:
            self.x_dir = False
        elif self.x_pos <= 0:
            self.x_dir = True

        # y-direction
        if self.y_dir:
            self.y_pos += 1.5 * self.speed
        elif not self.y_dir:
            self.y_pos += -1.5 * self.speed
        if self.y_pos >= 800:
            self.y_dir = False
        elif self.y_pos <= 0:
            self.y_dir = True


class Population():
    def __init__(self):
        self.foods = []
        self.blobs = [Blob(10, 10, 10, (200, 200, 200), 10, 10), Blob(6, 10, 10, (200, 200, 200), 50, 25)]

    def store_food(self, amount):  # creates a list of all the apples needed, each with different coordinates
        for x in range(amount):
            self.foods.append(Food(random.randint(0, 800), random.randint(0, 800)))

        return self.foods

    def replicate_blobs(self, blob):  # adds a blob to the population
        self.blobs.append(blob)

    # collision system
    def eat_food(self, food_population, blob_population):
        for blob in blob_population:
            for food in food_population:
                is_collision = self.check_collision(blob, food)
                if is_collision:
                    food_population.remove(food)

    def check_collision(self, blob, food):
        distance = (((blob.x_pos-food.x_pos) ** 2) + ((blob.y_pos-food.y_pos) ** 2)) ** 0.5
        if distance < (blob.size + food.radius) / 2.0:
            return True
        else:
            return False
        

