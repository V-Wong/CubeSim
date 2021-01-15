from typing import List

from copy import deepcopy

from .cube import Cube
from .move import Move
from .colour import WHITE, YELLOW, GREEN, BLUE, ORANGE, RED
from .history_cube import HistoryCube
from ..scramble.cleaner import clean_moves
from ..scramble.parser import scramble_to_moves, moves_to_scramble


def generate_solution(cube: Cube) -> List[Move]:
    cube_copy = HistoryCube(cube.size, deepcopy(cube.faces))

    solve_cross(cube_copy)
    solve_corners(cube_copy)
    solve_middle_edges(cube_copy)
    solve_eoll(cube_copy)
    solve_ocll(cube_copy)
    solve_cpll(cube_copy)
    solve_epll(cube_copy)

    return scramble_to_moves(clean_moves(moves_to_scramble(cube_copy.get_move_history())))


def solve_cross(cube: HistoryCube):
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
            cur_edge = tuple(cube.get_edge(edge).values())

            if cur_edge in [(colour, YELLOW), (YELLOW, colour)]:
                cube.do_moves(EDGES[edge])

                if cube.get_edge("UF")["U"] == YELLOW:
                    cube.do_moves("F2")
                else:
                    cube.do_moves("R U' R' F")

                cube.do_moves("D'")
                
                break

    cube.do_moves("D2")


def solve_corners(cube: Cube):
    CORNERS = {
        "UFR": "U2 U2",
        "DFR": "R U R' U'",
        "DBR": "R' U R U",
        "URB": "U",
        "ULF": "U'",
        "UBL": "U2",
        "DFL": "L' U' L",
        "DBL": "L U L' U" 
    }

    for colour1, colour2 in [(GREEN, RED), (BLUE, RED), 
                             (BLUE, ORANGE), (GREEN, ORANGE)]:
        for corner in CORNERS:
            cur_corner = cube.get_corner(corner).values()

            if colour1 in cur_corner and colour2 in cur_corner and YELLOW in cur_corner:
                cube.do_moves(CORNERS[corner])

                if cube.get_sticker("UFR") == YELLOW:
                    moves = "U R U2 R' U R U' R'"
                elif cube.get_sticker("FUR") == YELLOW:
                    moves = "U R U' R'"
                else:
                    moves = "R U R'"
                
                cube.do_moves(moves)
                cube.do_moves("D'")

                break
    

def solve_middle_edges(cube: Cube):
    EDGES = {
        "UF": "U2 U2",
        "UR": "U",
        "UL": "U'",
        "UB": "U2",
        "RF": "R' F R F' R U R' U'",
        "LF": "L F' L' F L' U' L U",
        "RB": "R' U R B' R B R'",
        "LB": "L U' L' B L' B' L"
    }

    for colour1, colour2 in [(GREEN, RED), (RED, BLUE), (BLUE, ORANGE), (ORANGE, GREEN)]:
        for edge in EDGES:
            cur_edge = tuple(cube.get_edge(edge).values())

            if cur_edge == (colour1, colour2) or cur_edge == (colour2, colour1):
                cube.do_moves(EDGES[edge])

                if cube.get_sticker("FU") == colour1:
                    moves = "U R U' R' F R' F' R"
                else:
                    moves = "U2 R' F R F' R U R'"
                cube.do_moves(moves)
                cube.do_moves("y")

                break


def solve_eoll(cube: Cube):
    for _ in range(4):
        top_layer = [cube.get_sticker("UB"), cube.get_sticker("UR"),
                     cube.get_sticker("UF"), cube.get_sticker("UL")]
        eo_state = [face == WHITE for face in top_layer]

        if eo_state == [False, False, False, False]:
            cube.do_moves("R U2 R2 F R F' U2 R' F R F'")
            break
        elif eo_state == [False, False, True, True]:
            cube.do_moves("U F U R U' R' F''")
            break
        elif eo_state == [False, True, False, True]:
            cube.do_moves("F R U R' U' F'")
            break
        else:
            cube.do_moves("U")


def solve_ocll(cube: Cube):
    OCLLS = {
        "S": "R U R' U R U2 R' U",
        "AS": "U R' U' R U' R' U2 R",
        "H": "F R U R' U' R U R' U' R U R' U' F'",
        "Headlights": "R2 D' R U2 R' D R U2 R",
        "Sidebars": "U' L F R' F' L' F R F'",
        "Fish": "R' U2 R' D' R U2 R' D R2",
        "Pi": "U R U2 R2 U' R2 U' R2 U2 R"
    }

    def get_top_layer_corners(cube: Cube):
        return [cube.get_sticker("UBL"), cube.get_sticker("UBR"),
                cube.get_sticker("UFR"), cube.get_sticker("UFL")]

    def get_co_state(top_layer):
        return [face == WHITE for face in top_layer]

    for _ in range(4):
        co_state = get_co_state(get_top_layer_corners(cube))

        if co_state == [False, False, False, False]:
            while cube.get_sticker("FUR") != WHITE or cube.get_sticker("FUL") != WHITE:
                cube.do_moves("U")

            if cube.get_corner("UFR")["F"] == cube.get_corner("UBL")["B"]: 
                cube.do_moves(OCLLS["H"])
            else:
                cube.do_moves(OCLLS["Pi"])
            break
        elif co_state == [False, False, False, True]:
            if cube.get_sticker("FUR") == WHITE:
                cube.do_moves(OCLLS["S"])
            else:
                cube.do_moves(OCLLS["AS"])
            break
        elif co_state == [False, False, True, True]:
            if cube.get_sticker("BRU") == WHITE:
                cube.do_moves(OCLLS["Headlights"])
            else:
                cube.do_moves(OCLLS["Sidebars"])
            break
        elif co_state == [False, True, False, True]:
            if cube.get_sticker("RUF") != WHITE:
                cube.do_moves("U2")
            cube.do_moves(OCLLS["Fish"])
            break
        else:
            cube.do_moves("U")


def solve_cpll(cube: Cube):
    alg = "R' U L' U2 R U' R' U2 R L "

    for _ in range(4):
        if cube.get_sticker("FUR") == cube.get_sticker("FUL") and cube.get_sticker("BLU") == cube.get_sticker("BRU"):
            break

        if cube.get_sticker("FRU") == cube.get_sticker("FLU"):
            cube.do_moves(alg)
            break
        cube.do_moves("U")
    else:
        cube.do_moves(alg + " U " + alg)


def solve_epll(cube: Cube):
    solved_edges = 0

    for _ in range(4):
        if cube.get_sticker("FU") == cube.get_sticker("FUR"):
            solved_edges += 1
        cube.do_moves("U")

    if solved_edges != 4:
        if solved_edges == 0:
            cube.do_moves("R U' R U R U R U' R' U' R2")

        while cube.get_sticker("FU") != cube.get_sticker("FUR"):
            cube.do_moves("U")

        cube.do_moves("U2")

        while cube.get_sticker("FU") != cube.get_sticker("FUR"):
            cube.do_moves("R U' R U R U R U' R' U' R2")

    while cube.get_sticker("FU") != cube.get_sticker("FR"):
        cube.do_moves("U") 