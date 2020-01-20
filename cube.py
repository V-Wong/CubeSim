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

    def rotate(self, face: str, prime: bool=False, double: bool=False):
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

    def y_rotate(self, invert: bool=False):
        l = [self.faces[face] for face in ["F", "L", "B", "R"]]

        self.faces["F"], self.faces["L"], \
        self.faces["B"], self.faces["R"] \
            = l[-1:] + l[:-1]

        self._face_rotate("U")
        self._face_rotate("D")
        self._face_rotate("D")
        self._face_rotate("D")

    def get_edge_info(self, piece: str) -> Tuple[int, int]:
        """
        We can information about an edge by doing moves to
        place it in UF, then analyse UF and undo the moves.
        """

        moves = scramble_to_moves({
                "UF": "U2 U2",
                "UL": "U'",
                "UR": "U",
                "UB": "U2",
                "LB": "L2 F",
                "LD": "L' F",
                "LF": "F",
                "RB": "R2 F'",
                "RD": "R F'",
                "RF": "F'",
                "DB": "D2 F2",
                "DF": "F2"
        }[piece])

        self._do_moves(moves)
        info = (self.faces["U"][-1][1], self.faces["F"][0][1])
        self._invert_moves(moves)

        return info

    def get_corner_info(self, piece: str) -> Tuple[int, int, int]:
        moves = scramble_to_moves({
                "UFR": "U2 U2",
                "DFR": "R",
                "DBR": "R2",
                "UBR": "R'",
                "UFL": "U'",
                "UBL": "U2",
                "DFL": "L' U'",
                "DBL": "L2 U'" 
        }[piece])

        self._do_moves(moves)
        info = (self.faces["U"][-1][-1], self.faces["F"][0][-1], self.faces["R"][0][0])
        self._invert_moves(moves)

        return info

    def _do_moves(self, moves: List[Tuple[str, bool, bool]]=[]):
        if isinstance(moves, str):
            moves = scramble_to_moves(moves)

        for move in moves:
            self.rotate(*move)

    def _invert_moves(self, moves: List[Tuple[str, bool, bool]]):
        for move in moves[::-1]:
            face, prime, double = move
            self.rotate(face, not prime, double)

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