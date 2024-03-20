"""Module for running the compost class."""

from dataclasses import dataclass, field


@dataclass
class Limit:
    """Utility class for setting limits."""

    min: float = field(default=0.0)
    max: float = field(default=float("inf"))

    def __post_init__(self):
        if self.min > self.max:
            raise ValueError(
                f"Minimum value ({self.min}) must be less than maximum value ({self.max})."
            )


@dataclass
class Property:
    """Class for a property of the compost."""

    name: str
    value: str

    theoretical_limit: Limit
    compliance_limit: Limit
