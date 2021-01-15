from typing import List

import random


def gen_n_scrambles(n: int) -> List[str]:
    scrambles = []

    for _ in range(n):
        scrambles.append(gen_scramble())

    return scrambles


def gen_scramble() -> str:
    moves = ["U", "R", "L", "B", "D", "F"]

    scramble = []

    for _ in range(40):
        rand_num = random.randint(0, 3) == 0

        if rand_num == 0:
            scramble.append(random.choice(moves))
        elif rand_num == 1:
            scramble.append(random.choice(moves) + "2")
        else:
            scramble.append(random.choice(moves) + "'")

    return " ".join(scramble)
