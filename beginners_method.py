from scramble_parser import scramble_to_moves
from cube import Cube
from cube import WHITE, YELLOW, GREEN, BLUE, ORANGE, RED



def solve_cross(cube: Cube):
    EDGES = {
        "UF": "",
        "UL": "U'",
        "UR": "U",
        "UB": "U2",
        "LB": "L U' L'",
        "LD": "L2 U'",
        "LF": "L' U' L",
        "RB": "R' U R",
        "RD": "R2 U",
        "RF": "R U R'",
        "DB": "B2 U2",
        "DF": "F2"
    }

    for colour in [BLUE, ORANGE, GREEN, RED]:
        for edge in EDGES:
            if (cube.get_edge_info(edge) == (colour, YELLOW)
                    or cube.get_edge_info(edge) == (YELLOW, colour)):
                cube._do_moves(scramble_to_moves(EDGES[edge]))

                if cube.get_edge_info("UF")[0] == YELLOW:
                    cube._do_moves(scramble_to_moves("F2"))
                else:
                    cube._do_moves(scramble_to_moves("R U' R' F"))

                cube._do_moves(scramble_to_moves("D'"))
                
                break

    cube._do_moves(scramble_to_moves("D2"))


def solve_corners(cube: Cube):
    CORNERS = {
        "UFR": "U2 U2",
        "DFR": "R U R' U'",
        "DBR": "R' U R U",
        "UBR": "R'",
        "UFL": "U'",
        "UBL": "U2",
        "DFL": "L' U' L",
        "DBL": "L U L' U" 
    }

    for colour1, colour2 in [(GREEN, RED), (BLUE, RED), (BLUE, ORANGE), (GREEN, ORANGE)]:
        for corner in CORNERS:
            cur_corner = cube.get_corner_info(corner)
            if (colour1 in cur_corner and colour2 in cur_corner and YELLOW in cur_corner):
                cube._do_moves(scramble_to_moves(CORNERS[corner]))
                cur_corner = cube.get_corner_info("UFR")
                if cur_corner[0] == YELLOW:
                    moves = scramble_to_moves("U R U2 R' U R U' R'")
                elif cur_corner[1] == YELLOW:
                    moves = scramble_to_moves("U R U' R'")
                elif cur_corner[2] == YELLOW:
                    moves = scramble_to_moves("R U R'")
                
                cube._do_moves(moves)
                cube._do_moves(scramble_to_moves("D'"))

                break

                