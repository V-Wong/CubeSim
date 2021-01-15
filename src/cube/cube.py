from typing import List, TypeVar, Union

from itertools import permutations

from .move import Move
from .colour import Colour, INITIAL_FACE_COLOUR_MAPPING
from .pieces import Corner, Edge, CORNER_TO_UFR, EDGE_TO_UF
from ..scramble import parser


class Cube:
    def __init__(self, size: int):
        self.size = size
        self.faces = {face: self._generate_face(colour, size) 
                      for face, colour in INITIAL_FACE_COLOUR_MAPPING}

    def get_sticker(self, sticker: str) -> Colour:
        for perm in permutations(sticker):
            if "".join(perm) in EDGE_TO_UF:
                return self.get_edge("".join(perm))[sticker[0]]
            elif "".join(perm) in CORNER_TO_UFR:
                return self.get_corner("".join(perm))[sticker[0]]

        raise ValueError(f"Not a valid sticker: {sticker}")

    def get_edge(self, piece: str) -> Edge:
        moves = parser.scramble_to_moves(EDGE_TO_UF[piece])

        self.do_moves(moves)
        info = Edge({
            piece[0]: Colour(self.faces["U"][-1][1]),
            piece[1]: Colour(self.faces["F"][0][1])
        })
        parser.invert_moves(moves)

        return info

    def get_corner(self, piece: str) -> Corner:
        moves = parser.scramble_to_moves(CORNER_TO_UFR[piece])

        self.do_moves(moves)
        info = Corner({
            piece[0]: Colour(self.faces["U"][-1][-1]), 
            piece[1]: Colour(self.faces["F"][0][-1]),
            piece[2]: Colour(self.faces["R"][0][0])
        })
        parser.invert_moves(moves)

        return info

    def do_moves(self, moves: Union[str, List[Move]]):
        if isinstance(moves, str):
            moves = parser.scramble_to_moves(moves)

        for move in moves:
            if move.face == "y":
                self._y_rotate()
            else:
                self._rotate(move)

    def is_solved(self) -> bool:
        for face in self.faces.values():
            for row in face:
                if any(piece_colour != face[0][0] for piece_colour in row):
                    return False

        return True

    def _generate_face(self, colour: Colour, size: int):
        return [[colour for _ in range(size)] for _ in range(size)]

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

        elif face == "F":
            l = [self.faces["U"], _transpose(self.faces["R"]),
                 self.faces["D"], _transpose(self.faces["L"])]
            r = [l[0][-1], l[1][0][::-1], l[2][0], l[3][-1][::-1]]

            l[0][-1], l[1][0], l[2][0], l[3][-1] = r[-1:] + r[:-1]

            self.faces["U"][-1] = l[0][-1]
            self.faces["R"] = _transpose(l[1])
            self.faces["D"][0] = l[2][0]
            self.faces["L"] = _transpose(l[3])

        elif face == "R":
            self._y_rotate()
            self._adjacent_face_swap("F")
            self._y_rotate(inverse=True)

        elif face == "L":
            self._y_rotate(inverse=True)
            self._adjacent_face_swap("F")
            self._y_rotate()

        elif face == "B":
            self._y_rotate(double=True)
            self._adjacent_face_swap("F")
            self._y_rotate(double=True)
            
    def _rotate(self, move: Move):
        for _ in range(2 if move.double else 3 if move.invert else 1):
            self._face_rotate(move.face)
            self._adjacent_face_swap(move.face)

    def _y_rotate(self, double=False, inverse=False):
        for i in range(2 if double else 3 if inverse else 1):
            l = [self.faces[face] for face in ["F", "L", "B", "R"]]
            self.faces["F"], self.faces["L"], self.faces["B"], self.faces["R"] = l[-1:] + l[:-1]

            self._face_rotate("U")
            for _ in range(3):
                self._face_rotate("D")
    

T = TypeVar("T")
def _transpose(l: List[List[T]]) -> List[List[T]]:
    return [list(i) for i in zip(*l)]
