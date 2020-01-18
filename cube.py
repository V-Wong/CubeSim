from typing import List

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

    def _face_rotate(self, face: str, counter_clockwise: bool):
        if not counter_clockwise:
            self.faces[face] = \
                    [list(row) for row in zip(*self.faces[face][::-1])]
        else:
            self.faces[face] = \
                    [list(row)[::-1] for row in zip(*(self.faces[face]))]

    def _adjacent_face_swap(self, face: str, counter_clockwise: bool):
        if face == "U":
            l = [self.faces["F"][0], self.faces["L"][0], \
                 self.faces["B"][0], self.faces["R"][0]]

            self.faces["F"][0], self.faces["L"][0], \
            self.faces["B"][0], self.faces["R"][0] \
                = l[1:] + l[:1] if counter_clockwise else l[-1:] + l[:-1]

        elif face == "D":
            l = [self.faces["F"][-1], self.faces["L"][-1], \
                 self.faces["B"][-1], self.faces["R"][-1]]

            self.faces["F"][-1], self.faces["L"][-1], \
            self.faces["B"][-1], self.faces["R"][-1] \
                = l[1:] + l[:1] if not counter_clockwise else l[-1:] + l[:-1]
