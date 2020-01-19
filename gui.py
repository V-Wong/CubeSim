from pprint import pprint
import time

import pygame
from pygame.locals import *

from cube import Cube
from scramble_parser import scramble_to_moves

HEIGHT = 1200
WIDTH = 1800
CUBIE_SIZE = 100


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
        for face_num, face in enumerate(["U", "F", "D", "B", "L", "R"]):
            for row_num, row in enumerate(self.cube.faces[face]):
                for cubie_num, cubie in enumerate(row):
                    if face == "L":
                        face_num = 1
                        horizontal_adjust = - self.cube.size * CUBIE_SIZE
                    elif face == "R":
                        face_num = 1
                        horizontal_adjust = self.cube.size * CUBIE_SIZE
                    elif face == "B":
                        face_num = 1
                        horizontal_adjust = 2 * self.cube.size * CUBIE_SIZE
                    else:
                        horizontal_adjust = 0
                        
                    pygame.draw.rect(self.screen, cubie,
                                     (WIDTH / 3 + cubie_num * CUBIE_SIZE + horizontal_adjust,
                                      self.cube.size * face_num * CUBIE_SIZE + row_num * CUBIE_SIZE,
                                      CUBIE_SIZE, CUBIE_SIZE), 0)
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (WIDTH / 3 + cubie_num * CUBIE_SIZE + horizontal_adjust,
                                      self.cube.size * face_num * CUBIE_SIZE + row_num * CUBIE_SIZE,
                                      CUBIE_SIZE, CUBIE_SIZE), 5)


if __name__ == "__main__":
    cube = Cube(3)
    scramble = scramble_to_moves("L' F' R D2 R D2 B2 F2 L R2 U2 R F2 U2 B' U' B' D B' U2 F'")
    for move in scramble:
        print(move)
        cube.rotate(*move)
    gui = Gui(cube)
    gui.run()