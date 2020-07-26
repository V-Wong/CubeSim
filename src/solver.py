from copy import deepcopy

from scramble_parser import scramble_to_moves
from cube import Cube
from cube import WHITE, YELLOW, GREEN, BLUE, ORANGE, RED


def generate_solution(cube: Cube):
    cube_copy = deepcopy(cube)

    solve_cross(cube_copy)
    solve_corners(cube_copy)
    solve_middle_edges(cube_copy)
    solve_eoll(cube_copy)
    solve_ocll(cube_copy)
    solve_cpll(cube_copy)
    solve_epll(cube_copy)

    return cube_copy.move_history


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
                cube.do_moves(EDGES[edge])

                if cube.get_edge_info("UF")[0] == YELLOW:
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
        "UBR": "U",
        "UFL": "U'",
        "UBL": "U2",
        "DFL": "L' U' L",
        "DBL": "L U L' U" 
    }

    for colour1, colour2 in [(GREEN, RED), (BLUE, RED), 
                            (BLUE, ORANGE), (GREEN, ORANGE)]:
        for corner in CORNERS:
            cur_corner = cube.get_corner_info(corner)
            if (colour1 in cur_corner and colour2 in cur_corner and YELLOW in cur_corner):
                cube.do_moves(CORNERS[corner])
                cur_corner = cube.get_corner_info("UFR")
                if cur_corner[0] == YELLOW:
                    moves = "U R U2 R' U R U' R'"
                elif cur_corner[1] == YELLOW:
                    moves = "U R U' R'"
                elif cur_corner[2] == YELLOW:
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
            cur_edge = cube.get_edge_info(edge)
            if (cur_edge == (colour1, colour2)
                    or cur_edge == (colour2, colour1)):
                cube.do_moves(EDGES[edge])
                cur_edge = cube.get_edge_info("UF")
                if cur_edge[1] == colour1:
                    moves = "U R U' R' F R' F' R"
                else:
                    moves = "U2 R' F R F' R U R'"
                cube.do_moves(moves)
                cube.do_moves("y")

                break


def solve_eoll(cube: Cube):
    for _ in range(4):
        top_layer = [cube.faces["U"][0][1], cube.faces["U"][1][2], 
                    cube.faces["U"][2][1], cube.faces["U"][1][0]]
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
        "Headlights": "R2 D' R U2 R' D R U2 R",
        "Sidebars": "U' L F R' F' L' F R F'",
        "Fish": "U' R' F R B' R' F' R B"
    }

    for _ in range(4):
        top_layer = [cube.faces["U"][0][0], cube.faces["U"][0][2], 
                    cube.faces["U"][2][0], cube.faces["U"][2][2]]
        co_state = [face == WHITE for face in top_layer]

        # For 0 oriented corners case, we can do sunes to generate
        # 1 or 2 oriented corner cases
        while co_state.count(True) == 0:
            cube.do_moves(OCLLS["S"])
            top_layer = [cube.faces["U"][0][0], cube.faces["U"][0][2], 
                        cube.faces["U"][2][0], cube.faces["U"][2][2]]
            co_state = [face == WHITE for face in top_layer]

        if co_state.count(True) == 2:
            while ((cube.faces["U"][2][0] != cube.faces["U"][2][2])
                    and cube.faces["U"][2][0] != cube.faces["U"][0][2]):
                cube.do_moves("U")
            if cube.faces["U"][2][0] == cube.faces["U"][2][2]:
                if cube.faces["B"][0][0] == WHITE:
                    cube.do_moves(OCLLS["Headlights"])
                else:
                    cube.do_moves(OCLLS["Sidebars"])
            else:
                while cube.faces["F"][0][2] != WHITE:
                    cube.do_moves("U")
                cube.do_moves(OCLLS["Fish"])
            break
        elif co_state.count(True) == 1:
            while cube.faces["U"][2][0] != WHITE:
                cube.do_moves("U")
            if cube.get_corner_info("UFR")[1] == WHITE:
                cube.do_moves(OCLLS["S"])
            else:
                cube.do_moves(OCLLS["AS"])
            break


def solve_cpll(cube: Cube):
    alg = "R' U L' U2 R U' R' U2 R L "

    for _ in range(4):
        if cube.faces["F"][0][0] == cube.faces["F"][0][2]:
            cube.do_moves(alg)
            break
        cube.do_moves("U")
    else:
        cube.do_moves(alg + " U " + alg)


def solve_epll(cube: Cube):
    if cube.faces["F"][0][1] != cube.faces["F"][0][2] or cube.faces["R"][0][1] != cube.faces["R"][0][2]:
        for _ in range(4):
            if cube.faces["B"][0][0] == cube.faces["B"][0][1]:
                while cube.faces["F"][0][0] != cube.faces["F"][0][1]:
                    cube.do_moves("R U' R U R U R U' R' U' R2")
                break
            cube.do_moves("U")
        else:
            for _ in range(4):
                cube.do_moves("R U' R U R U R U' R' U' R2")
                if cube.faces["B"][0][0] == cube.faces["B"][0][1]:
                    while cube.faces["F"][0][0] != cube.faces["F"][0][1]:
                        cube.do_moves("R U' R U R U R U' R' U' R2")
                    break
            cube.do_moves("U")
        
    while cube.faces["F"][0][1] != cube.faces["F"][1][1]:
        cube.do_moves("U")
