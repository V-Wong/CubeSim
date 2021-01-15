from typing import NewType, Dict, Literal

from .colour import Colour

Corner = NewType("Corner", Dict[str, Colour])
Edge = NewType("Edge", Dict[str, Colour])