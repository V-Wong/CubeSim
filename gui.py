from cube import Cube
import pygame
from pygame.locals import *

HEIGHT = 1600
WIDTH = 2000
CUBIE_SIZE = 100


class Gui:
    def __init__(self, cube: Cube):
        self.cube = cube
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def run(self):
        running = True
        while running:
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
                    else:
                        horizontal_adjust = 0
                        
                    pygame.draw.rect(self.screen, cubie,
                                     (WIDTH / 3 + cubie_num * CUBIE_SIZE + horizontal_adjust,
                                      self.cube.size * face_num * CUBIE_SIZE + row_num * CUBIE_SIZE,
                                      CUBIE_SIZE, CUBIE_SIZE), 1)


if __name__ == "__main__":
    cube = Cube(4)
    gui = Gui(cube)
    gui.run()