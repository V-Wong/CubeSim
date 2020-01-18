import numpy as np
from pprint import pprint

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


class Cube:
    def __init__(self, size: int):
        self.size = size

        self.faces = {
            "U": self._generate_face(WHITE, size),
            "F": self._generate_face(GREEN, size),
            "L": self._generate_face(ORANGE, size),
            "B": self._generate_face(BLUE, size),
            "R": self._generate_face(RED, size),
            "D": self._generate_face(YELLOW, size),
        }

    def _generate_face(self, colour: str, size: int):
        return [[colour for i in range(size)] for j in range(size)]

    def rotate(self):
        pass

    def face_rotate(self, face: str, counter_clockwise: bool):
        if not counter_clockwise:
            self.faces[face] = \
                    [list(row) for row in zip(*self.faces[face][::-1])]
        else:
            self.faces[face] = \
                    [list(row)[::-1] for row in zip(*(self.faces[face]))]
