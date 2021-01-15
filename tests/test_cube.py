from src.cube.cube import Cube
from src.cube.solver import generate_solution
from src.scramble.generator import gen_scramble
from src.scramble.parser import scramble_to_moves


def test_identity():
    cube = Cube(3)
    assert cube.is_solved()


def test_solve_invert_moves():
    for _ in range(100):
        cube = Cube(3)
        scramble = gen_scramble()
        cube.do_moves(scramble)
        cube._invert_moves(scramble_to_moves(scramble))
        assert cube.is_solved()


def test_solve_arbitrary_scrambles():
    for _ in range(1):
        cube = Cube(3)
        scramble = gen_scramble()
        cube.do_moves(scramble, save_history=False)
        solution = generate_solution(cube)
        cube.do_moves(solution)
        assert cube.is_solved()