from typing import Type, Callable

from openpyxl import Workbook

from cube import Cube
from scramble_generator import gen_scramble
from solver import generate_solution
from scramble_parser import moves_to_scramble

class Statistics:
    def __init__(self, cube_class: Type[Cube], scrambler: Callable, solver: Callable):
        self.cube_class = cube_class
        self.scrambler = scrambler
        self.solver = solver

        self.workbook = Workbook()
        self.worksheet = self.workbook.active

    def gen_headers(self):
        self.worksheet.append(["Scramble", "Length Of Solution", "Solution"])

    def generate_statistics(self, solves: int):
        for _ in range(solves):
            cur_cube = self.cube_class(3)
            scramble = self.scrambler()
            cur_cube.do_moves(scramble)
            solution = self.solver(cur_cube)
            self.worksheet.append([scramble, len(solution), 
                                   moves_to_scramble(solution)])

        self.workbook.save("cube_statistics.xlsx")


if __name__ == "__main__":
    stats = Statistics(Cube, gen_scramble, generate_solution)
    stats.gen_headers()
    stats.generate_statistics(100)