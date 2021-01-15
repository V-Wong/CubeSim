from typing import Type, Callable

from time import time
from openpyxl import Workbook

from ..cube.history_cube import HistoryCube
from ..cube.solver import generate_solution
from ..scramble.generator import gen_scramble
from ..scramble.parser import scramble_to_moves, moves_to_scramble
from ..scramble.cleaner import clean_moves

class Statistics:
    def __init__(self, cube_class: Type[HistoryCube], scrambler: Callable, solver: Callable):
        self.cube_class = cube_class
        self.scrambler = scrambler
        self.solver = solver

        self.workbook = Workbook()
        self.worksheet = self.workbook.active

    def gen_headers(self):
        self.worksheet.append(["Time Taken To Generate Solution", "Scramble", "Length Of Solution", "Solution"])

    def generate_statistics(self, solves: int):
        for _ in range(solves):
            cur_cube = self.cube_class(3)
            scramble = self.scrambler()
            cur_cube.do_moves(scramble, save_history=False)

            start_time = time()
            solution = scramble_to_moves(clean_moves(
                                         moves_to_scramble(self.solver(cur_cube))))
            end_time = time()

            solution_time = end_time - start_time

            self.worksheet.append([solution_time, scramble, len(solution), 
                                   moves_to_scramble(solution)])

        self.workbook.save("cube_statistics.xlsx")

if __name__ == "__main__":
    stats = Statistics(HistoryCube, gen_scramble, generate_solution)
    stats.gen_headers()
    stats.generate_statistics(100)