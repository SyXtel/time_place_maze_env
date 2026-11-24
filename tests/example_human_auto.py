from time_place_maze import TimePlaceMazeEnv
from maze_layout import MAZE_LAYOUT


env = TimePlaceMazeEnv(MAZE_LAYOUT, render_mode="human")

env.reset()
env.render()
env.step(3)
env.render()
env.step(3)
env.render()
env.step(3)
env.render()
env.step(0)
env.render()
env.step(4)
env.render()
env.close()