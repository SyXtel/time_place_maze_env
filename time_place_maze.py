import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
from maze_layout import MAZE_LAYOUT


class TimePlaceMazeEnv(gym.Env):

    def __init__(self, schema:list, render_mode:str = "ansi", fps: int = 5, debug: bool = False):
        super().__init__()

        self.render_mode = render_mode
        self.cell_size = 32
        self.fps = fps
        self.debug = debug

        self.window= None
        self.clock = None

        self.maze = np.array([list(row) for row in schema])
        self.height, self.width = self.maze.shape

        self.action_space = spaces.Discrete(5)
        
        self.observation_space = spaces.MultiDiscrete(
            [self.width, self.height]
        )

        self.action_to_direction = {
            0: np.array([-1, 0]),  # Left
            1: np.array([0, 1]),   # Down
            2: np.array([1, 0]),   # Right
            3: np.array([0, -1]),  # Up
            4: np.array([0, 0])    # Wait
        }

        y, x = np.argwhere(self.maze == 'S')[0]
        self.start_position = np.array([x, y], dtype=np.int64)
        self.agent_position = self.start_position.copy()

        if self.debug:
            print("Environment initialized.")
            print("Maze Layout:")
            print(self.print_state())
            print("Render Mode:", self.render_mode)
            print("FPS:", self.fps)
            print("\n")

    def _get_obs(self):
        return self.agent_position.copy()

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)

        self.agent_position = self.start_position.copy()
        self.info = {}

        if self.render_mode == "human":
            self._render_frame()

        if self.debug:
            print("Environment reset.")
            print("Maze Layout:")
            self.print_state()
            print("Start Position:", self.start_position)
            print("\n")

        return self._get_obs(), self.info

    def step(self, action):
        direction = self.action_to_direction[action]
        new_position = self.agent_position + direction

        x, y = new_position

        # Ensure the agent stays within bounds
        if 0 <= x < self.width and 0 <= y < self.height:
            # Check if the new position is a wall
            if self.maze[y, x] != '#':
                self.agent_position = new_position

        if self.render_mode == "human":
            self._render_frame()

        if self.debug:
            print("Action:", action)
            self.print_state()
            print("New Position:", self.agent_position)
            print("\n")

        return self._get_obs(), 0.0, False, False, {}

    def print_state(self):
        print(self.get_state())

    def get_state(self):
        grid = self.maze.copy()
        x, y = self.agent_position
        
        grid[y, x] = "A"

        return "\n".join(" ".join(row) for row in grid)

    def render(self):
        if self.render_mode == "ansi":
            return self.get_state()

        if self.render_mode == "human":
            self._render_frame()

    def _render_frame(self):
        """
        Renders the current state of the maze using pygame.
        """
        if self.window is None:
            pygame.init()

            self.window = pygame.display.set_mode((
                self.width * self.cell_size,
                self.height * self.cell_size
            ))

            pygame.display.set_caption("Time Place Maze")

            self.clock = pygame.time.Clock()

        colors = {
            '#': (0, 0, 0),        # Wall
            '.': (255, 255, 255),  # Floor
            'D': (255, 0, 0),      # Door
            'S': (0, 255, 0),      # Start
            'A': (0, 0, 255),      # Agent
            'R': (255, 255, 0)     # Reward
        }

        for y in range(self.height):
            for x in range(self.width):

                tile = self.maze[y, x]

                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                pygame.draw.rect(
                    self.window,
                    colors[tile],
                    rect
                )

        x, y = self.agent_position

        center = (
            int((x + 0.5) * self.cell_size),
            int((y + 0.5) * self.cell_size)
        )

        pygame.draw.circle(
            self.window,
            colors['A'],
            center,
            self.cell_size // 2
        )

        pygame.event.pump()
        pygame.display.flip()

        self.clock.tick(self.fps)

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

            self.window = None
            self.clock = None

        if self.debug:
            print("Environment closed.")
            print("\n")
