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

    def rotate(self, face: str, double: bool, prime: bool):
        if double:
            self._face_rotate(face, False)
            self._adjacent_face_swap(face, False)
            self._face_rotate(face, False)
            self._adjacent_face_swap(face, False)
        elif prime:
            for i in range(3):
                self._face_rotate(face, prime)
                self._adjacent_face_swap(face, prime)
        else:
            self._face_rotate(face, prime)
            self._adjacent_face_swap(face, prime)
            
    def _face_rotate(self, face: str, counter_clockwise: bool):
        if not counter_clockwise:
            self.faces[face] = \
                    [list(row) for row in zip(*self.faces[face][::-1])]
        else:
            self.faces[face] = \
                    [list(row) for row in zip(*(self.faces[face]))]

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

        elif face == "R":
            l = [self._transpose(l) for l in 
                                [self.faces["U"], self.faces["B"], self.faces["D"], self.faces["F"]]]
            r = [l[0][-1][::-1], l[1][0][::-1], l[2][-1], l[3][-1]]

            l[0][-1], l[1][0], l[2][-1], l[3][-1] = r[-1:] + r[:-1]

            for i, face in enumerate(["U", "B", "D", "F"]):
                self.faces[face] = self._transpose(l[i])

        elif face == "L":
            l = [self._transpose(l) for l in 
                                [self.faces["U"], self.faces["F"], self.faces["D"], self.faces["B"]]]
            r = [l[0][0], l[1][0], l[2][0][::-1], l[3][-1][::-1]]

            l[0][0], l[1][0], l[2][0], l[3][-1] = r[-1:] + r[:-1]

            for i, face in enumerate(["U", "F", "D", "B"]):
                self.faces[face] = self._transpose(l[i])

        elif face == "F":
            l = [self.faces["U"], self._transpose(self.faces["R"]), 
                 self.faces["D"], self._transpose(self.faces["L"])]
            r = [l[0][-1], l[1][0][::-1], l[2][0], l[3][-1][::-1]]

            l[0][-1], l[1][0], l[2][0], l[3][-1] \
                = r[-1:] + r[:-1]

            self.faces["U"][-1] = l[0][-1]
            self.faces["R"] = self._transpose(l[1])
            self.faces["D"][0] = l[2][0]
            self.faces["L"] = self._transpose(l[3])

        elif face == "B":
            l = [self.faces["U"], self._transpose(self.faces["R"]), 
                 self.faces["D"], self._transpose(self.faces["L"])]
            r = [l[0][0][::-1], l[1][-1], l[2][-1][::-1], l[3][0]]

            l[0][0], l[1][-1], l[2][-1], l[3][0] = r[1:] + r[:1]

            self.faces["U"][0] = l[0][0]
            self.faces["R"] = self._transpose(l[1])
            self.faces["D"][-1] = l[2][-1]
            self.faces["L"] = self._transpose(l[3])

    def _transpose(self, l: List[int]) -> List[int]:
        return [list(i) for i in zip(*l)]