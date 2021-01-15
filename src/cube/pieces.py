from typing import NewType, Dict, Literal

from .colour import Colour


Corner = NewType("Corner", Dict[str, Colour])
Edge = NewType("Edge", Dict[str, Colour])


EDGE_TO_UF = {
    "UF": "U2 U2",
    "UL": "U'",
    "UR": "U",
    "UB": "U2",
    "LB": "L2 F",
    "LD": "L' F",
    "LF": "F",
    "RB": "R2 F'",
    "RD": "R F'",
    "RF": "F'",
    "DB": "D2 F2",
    "DF": "F2"
}


CORNER_TO_UFR = {
    "UFR": "U2 U2",
    "DFR": "R",
    "DBR": "R2",
    "URB": "U",
    "ULF": "U'",
    "UBL": "U2",
    "DFL": "L' U'",
    "DBL": "L2 U'"
}
