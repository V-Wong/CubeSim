from pprint import pprint
import random


class Scrambler:
    def __init__(self):
        pass

    def gen_n_scrambles(self, n: int):
        scrambles = []

        for _ in range(n):
            scrambles.append(self.gen_scramble())

        return scrambles
    
    def gen_scramble(self):
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


if __name__ == "__main__":
    scrambler = Scrambler()
    pprint(scrambler.gen_n_scrambles(10))