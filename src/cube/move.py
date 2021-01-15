from dataclasses import dataclass


@dataclass
class Move:
    face: str
    invert: bool
    double: bool