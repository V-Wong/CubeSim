from typing import NewType, Tuple


Colour = NewType("Colour", Tuple[int, int, int])

WHITE = Colour((255, 255, 255))
GREEN = Colour((0, 255, 0))
ORANGE = Colour((255, 165, 0))
YELLOW = Colour((255, 255, 0))
BLUE = Colour((0, 0, 255))
RED = Colour((255, 0, 0))