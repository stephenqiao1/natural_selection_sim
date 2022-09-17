import pygame
import os
import SimEngine

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Natural Selection Simulation')

SCREEN_COLOR = pygame.Color('antiquewhite')
FPS = 60

FOOD = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'food_apple.png')), (20, 20))
NUM_OF_APPLES = 100


def draw_window(food):
    WIN.fill(SCREEN_COLOR)
    for apple in food.food_storage:
        WIN.blit(FOOD, apple)
    pygame.display.update()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    food = SimEngine.Food()
    run = True
    food.store_food(NUM_OF_APPLES)  # spawns the number of foods into the environment
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(food)
    pygame.quit()


if __name__ == "__main__":
    main()