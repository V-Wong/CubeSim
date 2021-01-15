from typing import List, Dict, Union

from .cube import Cube
from .pieces import Corner, Edge, EDGE_TO_UF, CORNER_TO_UFR
from .move import Move
from .colour import Colour
from ..scramble import parser


class HistoryCube(Cube):
    def __init__(self, size: int, faces: Dict[str, List[List[Colour]]]=None):
        super().__init__(size)

        self.faces = faces if faces else self.faces
        self._history = []

    def get_move_history(self) -> List[Move]:
        return self._history

    def get_edge(self, piece: str) -> Edge:
        moves = parser.scramble_to_moves(EDGE_TO_UF[piece])

        self.do_moves(moves, False)
        info = Edge({
            piece[0]: Colour(self.faces["U"][-1][1]),
            piece[1]: Colour(self.faces["F"][0][1])
        })
        self.do_moves(parser.invert_moves(moves), False)

        return info

    def get_corner(self, piece: str) -> Corner:
        moves = parser.scramble_to_moves(CORNER_TO_UFR[piece])

        self.do_moves(moves, False)
        info = Corner({
            piece[0]: Colour(self.faces["U"][-1][-1]), 
            piece[1]: Colour(self.faces["F"][0][-1]),
            piece[2]: Colour(self.faces["R"][0][0])
        })
        self.do_moves(parser.invert_moves(moves), False)

        return info

    def do_moves(self, moves: Union[str, List[Move]], save_history: bool=True): 
        super().do_moves(moves)

        if isinstance(moves, str):
            moves = parser.scramble_to_moves(moves)

        if save_history:
            for move in moves:
                self._history.append(move)
