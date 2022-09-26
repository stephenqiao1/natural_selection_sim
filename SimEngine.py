import random

DIE = 0
LIVE = 1
REPLICATE = 2
WIDTH, HEIGHT = 1400, 800

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
        self.foods_eaten = 0
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_dir = True  # True if it is moving in the right direction, otherwise False if going left
        self.y_dir = True  # True if it is moving in the downwards direction, otherwise False if going up
        self.home = (0, 0)
        self.age = 0

    def move_in_space(self):
        # x-direction
        if self.x_dir:
            self.x_pos += random.random() * self.speed
        elif not self.x_dir:
            self.x_pos += -1 * random.random() * self.speed
        if self.x_pos >= WIDTH:
            self.x_dir = False
        elif self.x_pos <= 0:
            self.x_dir = True

        # y-direction
        if self.y_dir:
            self.y_pos += random.random() * self.speed
        elif not self.y_dir:
            self.y_pos += -1 * random.random() * self.speed
        if self.y_pos >= HEIGHT:
            self.y_dir = False
        elif self.y_pos <= 0:
            self.y_dir = True


    def move_to_home(self):
        self.set_closest_home()

        x_dist = abs(self.x_pos - self.home[0])
        y_dist = abs(self.y_pos - self.home[1])

        if x_dist < y_dist:  # move in the horizontal direction
            if self.x_pos < 0:  # won't leave screen off the left side
                self.x_pos = 10
            if self.x_pos > WIDTH:
                self.x_pos = WIDTH - 10
            if self.x_pos < (WIDTH / 2):  # move left
                self.x_pos += -1 * self.speed
            else:
                self.x_pos += self.speed  # move right
        elif y_dist < x_dist:  # move in the vertical direction
            if self.y_pos < 0:
                self.y_pos = 10
            if self.y_pos > HEIGHT:
                self.y_pos = HEIGHT - 10
            if self.y_pos < (HEIGHT / 2):  # move up
                self.y_pos += -1 * self.speed
            else:
                self.y_pos += self.speed  # move down

    def set_closest_home(self):
        dist_top_edge = self.y_pos
        dist_bot_edge = HEIGHT - self.y_pos
        dist_left_edge = self.x_pos
        dist_right_edge = WIDTH - self.x_pos

        dist_all_edges = [dist_top_edge, dist_bot_edge, dist_left_edge, dist_right_edge]

        top_home_pos = (self.x_pos, 0)  # index 0
        bot_home_pos = (self.x_pos, HEIGHT)  # index 1
        left_home_pos = (0, self.y_pos)  # index 2
        right_home_pos = (WIDTH, self.y_pos)  # index 3

        all_home_pos = [top_home_pos, bot_home_pos, left_home_pos, right_home_pos]

        current_dist = 2000  # this will keep track of the lowest distance
        index = 0

        for edge in dist_all_edges:
            if edge < current_dist:
                current_dist = edge
                self.home = all_home_pos[index]
                return
            index += 1


class Population():
    def __init__(self):
        self.foods = []
        self.blobs = [Blob(10, 10, 10, (200, 200, 200), 400, 500), Blob(10, 10, 10, (200, 200, 200), 20, 350)]
        self.blobs_population_size = 1

    def store_food(self, amount):  # creates a list of all the apples needed, each with different coordinates
        for x in range(amount):
            self.foods.append(Food(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

        return self.foods


    def move_all_blobs_home(self):
        for blob in self.blobs:
            blob.move_to_home()


    def move_all_blobs(self):
        for blob in self.blobs:
            blob.move_in_space()

    '''
    Decides the life of the blob at end of day
    '''
    def decide_blobs_life(self, blob_population, population_size):
        for blob in blob_population:
            if blob.foods_eaten == DIE and blob.age != 0:
                blob_population.remove(blob)
                print('blob died')
        if population_size > 0:       
            for x in range(population_size):
                new_blob = self.mutate(blob_population[x])
                if len(blob_population) < population_size:
                    blob_population.append(new_blob)
    
    def update_blob_population(self):
        for blob in self.blobs:
            if blob.foods_eaten >= REPLICATE:
                self.blobs_population_size += 1
            elif blob.foods_eaten == DIE and blob.age != 0:
                self.blobs_population_size -= 1
                     
                
    '''
    Mutation system
    '''
    def mutate(self, blob): 
        if random.random() <= 0.05: # 5% mutation rate
            mutation_option = random.randint(0, 2)
            if mutation_option == 0:  # mutate speed gene
                return Blob(random.uniform(-100, 100), blob.size, blob.sense, blob.color, blob.x_pos, random.randint(0, HEIGHT))
            elif mutation_option == 1:  # mutate size gene
                return Blob(blob.speed, random.uniform(0, 100), blob.sense, blob.color, blob.x_pos, random.randint(0, HEIGHT))
            elif mutation_option == 2:  # mutate sense gene
                return Blob(blob.speed, blob.size, random.uniform(0, 50), blob.color, blob.x_pos, random.randint(0, HEIGHT))
        else:
            return Blob(blob.speed, blob.size, blob.sense, blob.color, blob.x_pos, random.randint(0, HEIGHT))
        
    # collision system
    def eat_food(self, food_population, blob_population):
        for blob in blob_population:
            for food in food_population:
                is_collision = self.check_collision(blob, food)
                if is_collision:
                    food_population.remove(food)
                    blob.foods_eaten += 1

    def check_collision(self, blob, food):
        distance = (((blob.x_pos-food.x_pos) ** 2) + ((blob.y_pos-food.y_pos) ** 2)) ** 0.5
        if distance < (blob.size + food.radius) / 2.0:
            return True
        else:
            return False
