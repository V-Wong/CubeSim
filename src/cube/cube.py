from typing import List, Tuple, TypeVar, Union

from .colour import Colour, WHITE, GREEN, ORANGE, BLUE, RED, YELLOW
from ..scramble import parser


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
        self.move_history = []

    def get_edge_info(self, piece: str) -> Tuple[int, int]:
        """
        We can information about an edge by doing moves to
        place it in UF, then analyse UF and undo the moves.
        """

        moves = parser.scramble_to_moves({
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

        self.do_moves(moves, False)
        info = self.faces["U"][-1][1], self.faces["F"][0][1]
        self._invert_moves(moves, False)

        return info

    def get_corner_info(self, piece: str) -> Tuple[int, int, int]:
        moves = parser.scramble_to_moves({
            "UFR": "U2 U2",
            "DFR": "R",
            "DBR": "R2",
            "UBR": "R'",
            "UFL": "U'",
            "UBL": "U2",
            "DFL": "L' U'",
            "DBL": "L2 U'"
        }[piece])

        self.do_moves(moves, False)
        info = (self.faces["U"][-1][-1], self.faces["F"][0][-1], self.faces["R"][0][0])
        self._invert_moves(moves, False)

        return info

    def do_moves(self, moves: Union[str, Tuple[int, int, int]], save_history: bool = True):
        if isinstance(moves, str):
            moves = parser.scramble_to_moves(moves)

        for move in moves:
            if move[0] == "y":
                self._y_rotate()
            else:
                self._rotate(*move)

            if save_history:
                self.move_history.append(move)

    def _generate_face(self, colour: Colour, size: int):
        return [[colour for i in range(size)] for j in range(size)]

    def _face_rotate(self, face: str):
        self.faces[face] = [list(row) for row in zip(*self.faces[face][::-1])]

    def _adjacent_face_swap(self, face: str):
        if face == "U":
            l = [self.faces[face][0] for face in ["F", "L", "B", "R"]]

            self.faces["F"][0], self.faces["L"][0], \
                self.faces["B"][0], self.faces["R"][0] = l[-1:] + l[:-1]

        elif face == "D":
            l = [self.faces[face][-1] for face in ["F", "L", "B", "R"]]

            self.faces["F"][-1], self.faces["L"][-1], \
                self.faces["B"][-1], self.faces["R"][-1] = l[1:] + l[:1]

        elif face == "R":
            l = [_transpose(l) for l in
                 [self.faces[face] for face in ["U", "B", "D", "F"]]]
            r = [l[0][-1][::-1], l[1][0][::-1], l[2][-1], l[3][-1]]

            l[0][-1], l[1][0], l[2][-1], l[3][-1] = r[-1:] + r[:-1]

            for i, face in enumerate(["U", "B", "D", "F"]):
                self.faces[face] = _transpose(l[i])

        elif face == "L":
            l = [_transpose(l) for l in
                 [self.faces[face] for face in ["U", "F", "D", "B"]]]
            r = [l[0][0], l[1][0], l[2][0][::-1], l[3][-1][::-1]]

            l[0][0], l[1][0], l[2][0], l[3][-1] = r[-1:] + r[:-1]

            for i, face in enumerate(["U", "F", "D", "B"]):
                self.faces[face] = _transpose(l[i])

        elif face == "F":
            l = [self.faces["U"], _transpose(self.faces["R"]),
                 self.faces["D"], _transpose(self.faces["L"])]
            r = [l[0][-1], l[1][0][::-1], l[2][0], l[3][-1][::-1]]

            l[0][-1], l[1][0], l[2][0], l[3][-1] = r[-1:] + r[:-1]

            self.faces["U"][-1] = l[0][-1]
            self.faces["R"] = _transpose(l[1])
            self.faces["D"][0] = l[2][0]
            self.faces["L"] = _transpose(l[3])

        elif face == "B":
            l = [self.faces["U"], _transpose(self.faces["R"]),
                 self.faces["D"], _transpose(self.faces["L"])]
            r = [l[0][0][::-1], l[1][-1], l[2][-1][::-1], l[3][0]]

            l[0][0], l[1][-1], l[2][-1], l[3][0] = r[1:] + r[:1]

            self.faces["U"][0] = l[0][0]
            self.faces["R"] = _transpose(l[1])
            self.faces["D"][-1] = l[2][-1]
            self.faces["L"] = _transpose(l[3])

    def _rotate(self, face: str, prime: bool = False, double: bool = False):
        if double:
            for _ in range(2):
                self._face_rotate(face)
                self._adjacent_face_swap(face)
        elif prime:
            for _ in range(3):
                self._face_rotate(face)
                self._adjacent_face_swap(face)
        else:
            self._face_rotate(face)
            self._adjacent_face_swap(face)

    def _invert_moves(self, moves: List[Tuple[str, bool, bool]], save_history: bool = True):
        for move in reversed(moves):
            if save_history:
                self.move_history.append(move)
            face, prime, double = move
            self._rotate(face, not prime, double)

    def _y_rotate(self, invert: bool = False):
        l = [self.faces[face] for face in ["F", "L", "B", "R"]]

        self.faces["F"], self.faces["L"], self.faces["B"], self.faces["R"] = l[-1:] + l[:-1]

        self._face_rotate("U")
        self._face_rotate("D")
        self._face_rotate("D")
        self._face_rotate("D")

        self.move_history.append(("y", False, False))

T = TypeVar("T")
def _transpose(l: List[List[T]]) -> List[List[T]]:
    return [list(i) for i in zip(*l)]
