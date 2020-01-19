from typing import List, Tuple

import numpy as np
from pprint import pprint

from scramble_parser import scramble_to_moves

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

        self.scramble = None

    def _generate_face(self, colour: str, size: int):
        return [[colour for i in range(size)] for j in range(size)]

    def rotate(self, face: str, prime: bool, double: bool):
        if double:
            self._face_rotate(face)
            self._adjacent_face_swap(face)
            self._face_rotate(face)
            self._adjacent_face_swap(face)
        elif prime:
            for i in range(3):
                self._face_rotate(face)
                self._adjacent_face_swap(face)
        else:
            self._face_rotate(face)
            self._adjacent_face_swap(face)
            
    def _face_rotate(self, face: str):
        self.faces[face] = \
                [list(row) for row in zip(*self.faces[face][::-1])]

    def _adjacent_face_swap(self, face: str):
        if face == "U":
            l = [self.faces[face][0] for face in ["F", "L", "B", "R"]]
            
            self.faces["F"][0], self.faces["L"][0], \
            self.faces["B"][0], self.faces["R"][0] \
                = l[-1:] + l[:-1]

        elif face == "D":
            l = [self.faces[face][-1] for face in ["F", "L", "B", "R"]]

            self.faces["F"][-1], self.faces["L"][-1], \
            self.faces["B"][-1], self.faces["R"][-1] \
                = l[1:] + l[:1]

        elif face == "R":
            l = [self._transpose(l) for l in 
                 [self.faces[face] for face in ["U", "B", "D", "F"]]]
            r = [l[0][-1][::-1], l[1][0][::-1], l[2][-1], l[3][-1]]

            l[0][-1], l[1][0], l[2][-1], l[3][-1] = r[-1:] + r[:-1]

            for i, face in enumerate(["U", "B", "D", "F"]):
                self.faces[face] = self._transpose(l[i])

        elif face == "L":
            l = [self._transpose(l) for l in 
                 [self.faces[face] for face in ["U", "F", "D", "B"]]]
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

    def set_scramble(self, scramble: str):
        self.scramble = scramble_to_moves(scramble)
        for move in self.scramble:
            self.rotate(*move)

    def cheat_solve(self) -> List[Tuple[str, bool, bool]]:
        solution = []

        for move in self.scramble[::-1]:
            face, prime, double = move
            solution.append((face, not prime, double))

        return solution