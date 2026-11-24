from time_place_maze import TimePlaceMazeEnv
from maze_layout import MAZE_LAYOUT


env = TimePlaceMazeEnv(MAZE_LAYOUT, render_mode="ansi", debug=True)

env.reset()
env.step(3)
env.step(3)
env.step(3)
env.step(0)
env.step(4)
env.close()
