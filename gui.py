from pprint import pprint
import time

import pygame
from pygame.locals import *

from cube import Cube
from scramble_parser import scramble_to_moves
from beginners_method import solve_cross, solve_corners, solve_middle_edges, solve_eoll, solve_ocll, solve_cpll, solve_epll

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
                prime = pygame.key.get_pressed()[pygame.K_LSHIFT]
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)

                    if key in {"u", "f", "l", "r", "d", "b"}:
                        self.cube.rotate(key.upper(), prime, False)

                    if event.key == pygame.K_SPACE:
                        for move in self.cube.cheat_solve():
                            self.cube.rotate(*move)
                            self.draw_cube()
                            time.sleep(0.1)

            self.draw_cube()
            
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
                    y = self.cube.size * face_num * CUBIE_SIZE + row_num * CUBIE_SIZE
                    
                    pygame.draw.rect(self.screen, cubie, (x, y, CUBIE_SIZE, CUBIE_SIZE), 0)
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, CUBIE_SIZE, CUBIE_SIZE), 5)

        pygame.display.update()

if __name__ == "__main__":
    cube = Cube(3)
    scramble = "U2 L F B R F2 B2 R U D2 F2 L2 F D2 B' R2 F' D2 F U2 B2"
    cube.set_scramble(scramble)
    solve_cross(cube)
    solve_corners(cube)
    solve_middle_edges(cube)
    solve_eoll(cube)
    solve_ocll(cube)
    solve_cpll(cube)
    solve_epll(cube)
    gui = Gui(cube)
    gui.run()