import pygame

from time_place_maze import TimePlaceMazeEnv
from maze_layout import MAZE_LAYOUT

env = TimePlaceMazeEnv(MAZE_LAYOUT, render_mode="human")
env.reset()

key_to_action = {
    pygame.K_LEFT: 0,
    pygame.K_DOWN: 1,
    pygame.K_RIGHT: 2,
    pygame.K_UP: 3,
    pygame.K_SPACE: 4
}

running = True

while running:

    event = pygame.event.wait()

    if event.type == pygame.QUIT:
        running = False

    elif event.type == pygame.KEYDOWN:

        if event.key == pygame.K_ESCAPE:
            running = False

        elif event.key == pygame.K_r:
            env.reset()

        elif event.key in key_to_action:
            env.step(key_to_action[event.key])

env.close()