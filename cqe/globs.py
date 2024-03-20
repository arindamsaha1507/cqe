from enum import Enum


MAX_SCORE = 5.0


class Grades(Enum):
    """Enum for the grades of compost."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    RU1 = "RU1"
    RU2 = "RU2"
    RU3 = "RU3"


class CategoryType(Enum):
    """Enum for the type of category."""

    INCREASING = "increasing"
    DECREASING = "decreasing"


class IndexType(Enum):
    """Enum for the type of index."""

    CLEAN = "clean"
    FERTILITY = "fertility"
