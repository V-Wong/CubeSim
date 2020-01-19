from typing import Tuple

from pprint import pprint
import math
import time

import pygame
from pygame.locals import *

from cube import Cube
from scramble_parser import scramble_to_moves

HEIGHT = 1600
WIDTH = 1800
CUBIE_SIZE = 100

ANGLE = math.cos(0.1)


class Gui:
    def __init__(self, cube: Cube):
        self.cube = cube
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = sys.exit()

                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)

                    if key in {"u", "f", "l", "r", "d", "b"}:
                        self.cube.rotate(key.upper(), False, False)

            self.draw_cube()
            pygame.display.update()

    def draw_cube(self):
        rect = None
        for face_num, face in enumerate(["U"]):
            for row_num, row in enumerate(self.cube.faces[face]):
                for cubie_num, cubie in enumerate(row):
                    if face == "L":
                        face_num = 1
                        horizontal_adjust = - self.cube.size * CUBIE_SIZE
                    elif face == "R":
                        face_num = 1
                        horizontal_adjust = self.cube.size * CUBIE_SIZE
                    else:
                        horizontal_adjust = 0

                    if not rect:
                        rect = pygame.draw.rect(self.screen, (0, 255, 255),
                            (WIDTH / 3 + cubie_num * CUBIE_SIZE,
                            self.cube.size * face_num * CUBIE_SIZE + row_num * CUBIE_SIZE,
                            CUBIE_SIZE, CUBIE_SIZE), 0)

                    top_left = self._rotate_point((rect.x, rect.y))
                    top_right = self._rotate_point((rect.x + rect.width, rect.y))
                    bot_left = self._rotate_point((rect.x, rect.y + rect.height))
                    bot_right = self._rotate_point((rect.x + rect.width, rect.y + rect.height))

                    rect = pygame.draw.polygon(self.screen, (255, 255, 255), (top_left, bot_left, bot_right, top_right))

    def _rotate_point(self, point: Tuple[int, int]) -> Tuple[int, int]:
        x, y = point[0], point[1]
        return (x * math.cos(0.5) - y * math.sin(0.5), x * math.sin(0.5) + y * math.cos(0.5))

if __name__ == "__main__":
    cube = Cube(2)
    # scramble = scramble_to_moves("F R' F2 U R' F R U2 R'")
    # for move in scramble:
    #     print(move)
    #     cube.rotate(*move)
    gui = Gui(cube)
    gui.run()