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


def draw_window(food, blob_population):
    WIN.fill(SCREEN_COLOR)
    for apple in food:
        WIN.blit(FOOD, (apple.x_pos, apple.y_pos))
    for blob in blob_population:
        pygame.draw.circle(WIN, blob.color, (blob.x_pos, blob.y_pos), blob.size)
    pygame.display.update()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    food_storage = SimEngine.Population().store_food(NUM_OF_APPLES)  # spawns the number of foods into the environment
    blob_population = SimEngine.Population().blobs
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for blob in blob_population:
            blob.move_in_space()
        draw_window(food_storage, blob_population)
    pygame.quit()


if __name__ == "__main__":
    main()