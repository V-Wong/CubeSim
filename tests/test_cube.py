import sys
sys.path.append("../src")

from cube import Cube
from scramble_generator import gen_scramble
from solver import generate_solution


def is_solved(cube: Cube) -> bool:
    for face in cube.faces.values():
        for row in face:
            if any(piece_colour != face[0][0] for piece_colour in row):
                return False

    return True


def test_identity():
    solved_cube = Cube(3)
    assert is_solved(solved_cube)


def test_solve_arbitrary_scrambles():
    for _ in range(1):
        cube = Cube(3)
        scramble = gen_scramble()
        cube.set_scramble(scramble)
        solution = generate_solution(cube)
        cube.do_moves(solution)
        assert is_solved(cube)