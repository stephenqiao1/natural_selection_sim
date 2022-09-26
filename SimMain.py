import pygame
import os
import SimEngine
import time

WIDTH, HEIGHT = 1400, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Natural Selection Simulation')

SCREEN_COLOR = pygame.Color('antiquewhite')
FPS = 60

FOOD = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'food_apple.png')), (20, 20))
NUM_OF_APPLES = 5

REST_TIME = 10
SETUP_TIME = 15
RESET_TIME = 20

populations = SimEngine.Population()
food_storage = populations.store_food(NUM_OF_APPLES)  # spawns the number of foods into the environment
blob_population = populations.blobs

def draw_window(food, blob_population, text):
    WIN.fill(SCREEN_COLOR)
    WIN.blit(text, (0,0))
    for apple in food:
        WIN.blit(FOOD, (apple.x_pos, apple.y_pos))
    for blob in blob_population:
        pygame.draw.circle(WIN, blob.color, (blob.x_pos, blob.y_pos), blob.size)
    pygame.display.update()

'''
Day and night system
'''
def day_cycle(elapsed_time, updated):
    if elapsed_time >= REST_TIME and elapsed_time < RESET_TIME:
        populations.move_all_blobs_home()  # move all blobs to their home spot
    if updated == False:
        populations.update_blob_population()   
    if elapsed_time == SETUP_TIME:
        if len(food_storage) < NUM_OF_APPLES:
            populations.store_food(NUM_OF_APPLES)
        populations.decide_blobs_life(blob_population, populations.blobs_population_size)


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

def main():
    pygame.init()
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    start_time = time.time()
    clock = pygame.time.Clock()
    day = 0
    updated = False
    run = True
    while run:
        clock.tick(FPS)
        text_surface = my_font.render('Day ' + str(day), False, (0, 0, 0))
        elapsed_time = round(time.time() - start_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        populations.eat_food(food_storage, blob_population)
        if elapsed_time >= 0 and elapsed_time < REST_TIME:
            populations.move_all_blobs()
        elif elapsed_time >= REST_TIME and elapsed_time < RESET_TIME:
            day_cycle(elapsed_time, updated)
            updated = True
        if elapsed_time == RESET_TIME:  # resets timer
            print("blob population: " + str(populations.blobs_population_size))
            day += 1
            for blob in blob_population:
                blob.age += 1
                blob.foods_eaten = 0
            start_time = time.time()
            updated = False
        print(elapsed_time)
        draw_window(food_storage, blob_population, text_surface)
    pygame.quit()


if __name__ == "__main__":
    main()