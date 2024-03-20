"""Module for the index of the compost."""

from dataclasses import dataclass, field

from cqe.globs import CategoryType, IndexType, MAX_SCORE


@dataclass
class Index:
    """Class for an index of the compost."""

    typ: IndexType
    weight: float
    category_limits: list[float]
    category_type: CategoryType = field(init=False)
    score: float = field(init=False)

    def __post_init__(self):

        if self.category_limits == sorted(self.category_limits):
            self.category_type = CategoryType.INCREASING
        elif self.category_limits == sorted(self.category_limits, reverse=True):
            self.category_type = CategoryType.DECREASING
        else:
            raise ValueError(
                "Category limits must be in increasing or decreasing order."
            )

    def set_score(self, value: float):
        """Set the score of the index."""
        self.score = MAX_SCORE
        if self.category_type == CategoryType.INCREASING:
            for limit in self.category_limits:
                if value > limit:
                    self.score -= 1

        elif self.category_type == CategoryType.DECREASING:
            for limit in self.category_limits:
                if value < limit:
                    self.score -= 1
