import random

DIE = 0
LIVE = 1
REPLICATE = 2
WIDTH, HEIGHT = 1400, 800
ENERGY_LEVEL = 1000000000 # 1 billion
MUTATION_RATE = 0.05 # 3% mutation rate

class Food():
    def __init__(self, x, y):
        self.food_score = 1
        self.radius = 5
        self.x_pos = x
        self.y_pos = y

class Blob():
    def __init__(self, speed, radius, color, x_pos, y_pos):
        self.speed = speed
        self.size = radius
        self.energy = ENERGY_LEVEL
        self.foods_eaten = 0
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_dir = True  # True if it is moving in the right direction, otherwise False if going left
        self.y_dir = True  # True if it is moving in the downwards direction, otherwise False if going up
        self.home = (0, 0)
        self.age = 0

    def move_in_space(self):
        self.energy_depletion()
        if self.energy > 0:
             # x-direction
            self.x_pos += random.uniform(-1, 1) * self.speed
            
            if self.x_pos >= WIDTH:
                self.x_pos = WIDTH
            elif self.x_pos <= 0:
                self.x_pos = 0

            # y-direction
            self.y_pos += 1 * random.uniform(-1, 1) * self.speed
            
            if self.y_pos >= HEIGHT:
                self.y_pos = HEIGHT
            elif self.y_pos <= 0:
                self.y_pos = 0
        
        

    def move_to_home(self): # needs to change 
        self.set_closest_home()
        
        if self.home == (self.x_pos, 0):
            if self.y_pos <= 10:
                self.y_pos = 10
            else:
                self.y_pos += -1 * self.speed
        elif self.home == (self.x_pos, HEIGHT):
            if self.y_pos >= (HEIGHT - 10):
                self.y_pos = HEIGHT - 10
            else:
                self.y_pos += 1 * self.speed
        elif self.home == (0, self.y_pos):
            if self.x_pos <= 10:
                self.x_pos = 10
            else:
                self.x_pos += 1 * self.speed
        elif self.home == (WIDTH, self.y_pos):
            if self.x_pos >= WIDTH - 10:
                self.x_pos = WIDTH - 10
            else:
                self.x_pos += -1 * self.speed
                

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
            index += 1
            
    '''
    Energy Cost System
    '''
    def energy_depletion(self):
        self.energy -= (self.size ** 3) * (self.speed ** 2)
        

class Population():
    def __init__(self):
        self.foods = []
        self.blobs = [Blob(10, 5, (0, 255, 0), 400, 500)]
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
        if population_size > 0:       
            for x in range(population_size):
                new_blob = self.mutate(blob_population[x])
                if len(blob_population) < population_size:
                    blob_population.append(new_blob)
    
    def update_blob_population(self):
        for blob in self.blobs:
            if blob.foods_eaten >= REPLICATE:
                self.blobs_population_size += 1
                print('blob replicated')
            elif blob.foods_eaten == DIE and blob.age != 0:
                self.blobs_population_size -= 1
                print('blob died')
                     
                
    '''
    Mutation system
    '''
    def mutate(self, blob): 
        if random.random() <= MUTATION_RATE: 
            mutation_option = random.randint(0, 1)
            if mutation_option == 0:  # mutate speed gene
                return Blob(random.uniform(0, 50), blob.size, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)), blob.x_pos, blob.y_pos)
            elif mutation_option == 1:  # mutate size gene
                return Blob(blob.speed, random.uniform(0, 100), (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)), blob.x_pos, blob.y_pos)
            print('mutation!')
        else:
            return Blob(blob.speed, blob.size, blob.color, blob.x_pos, blob.y_pos)
        
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
