from pprint import pprint
import time

import pygame
from pygame.locals import *

from .cube import Cube
from ..scramble.parser import scramble_to_moves, moves_to_scramble
from ..scramble.generator import gen_scramble
from ..scramble.cleaner import clean_moves
from .solver import generate_solution

HEIGHT = 1440
WIDTH = 2415
CUBIE_SIZE = 125
HORIZONTAL_START = 100

class Gui:
    def __init__(self, cube: Cube):
        self.cube = cube
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def run(self):
        self.draw_cube()

        running = True
        while running:
            for event in pygame.event.get():
                prime = pygame.key.get_pressed()[pygame.K_LSHIFT]
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)

                    if key in {"u", "f", "l", "r", "d", "b"}:
                        self.cube._rotate(key.upper(), prime, False)
                        self.draw_cube()
                    elif key == "s":
                        self.cube = Cube(3)
                        self.cube.do_moves(gen_scramble(), save_history=False)
                        self.draw_cube()
                    elif event.key == pygame.K_SPACE:
                        solution = clean_moves(moves_to_scramble(
                                               generate_solution(self.cube)))
                        for move in solution.split():
                            self.cube.do_moves(move)
                            self.draw_cube()
                            time.sleep(0.01)
            
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
                        
                    x = WIDTH / 3 + cubie_num * CUBIE_SIZE + horizontal_adjust
                    y = self.cube.size * face_num * CUBIE_SIZE + row_num * CUBIE_SIZE + HORIZONTAL_START
                    
                    pygame.draw.rect(self.screen, cubie, (x, y, CUBIE_SIZE, CUBIE_SIZE), 0)
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, CUBIE_SIZE, CUBIE_SIZE), 5)

        pygame.display.update()
