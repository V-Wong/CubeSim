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
