"""Module to handle properties of compost."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Identity:
    """Identity class for property."""

    name: str
    value: float
    units: str


@dataclass
class Limits:
    """Class to handle compost properties."""

    min_value: Optional[float] = None
    max_value: Optional[float] = None

    def __post_init__(self):
        """Post init method to handle derived properties."""

        if self.min_value is None and self.max_value is None:
            raise ValueError("Either min_value or max_value should be specified.")

        if self.min_value is None:
            self.min_value = float("-inf")

        if self.max_value is None:
            self.max_value = float("inf")

        if self.min_value > self.max_value:
            raise ValueError("min_value should be less than max_value.")

    def validate(self, identity: Identity):
        """Helper function to validate if a value is within a specified range."""

        parameter_name = identity.name
        value = identity.value
        min_value = self.min_value
        max_value = self.max_value

        if value < min_value or value > max_value:
            raise ValueError(
                f"{parameter_name} should be between {min_value} and {max_value}."
            )

    def is_compliant(self, value: float):
        """Helper function to check if a value is within a specified range."""

        min_value = self.min_value
        max_value = self.max_value

        return min_value <= value <= max_value


@dataclass
class Scores:
    """Class to handle chemical properties of compost."""

    weight: float
    limits: list[float]
    category: int = field(init=False)
    ascending: bool = field(init=False)

    def __post_init__(self):
        """Post init method to handle derived properties."""

        if self.limits == sorted(self.limits):
            self.ascending = True
        elif self.limits == sorted(self.limits, reverse=True):
            self.ascending = False
        else:
            raise ValueError("Limits should be either ascending or descending.")

    def assign_category(self, value, clean=False):
        """Assign category to fertility property."""

        limits = self.limits
        self.category = len(limits) if clean else len(limits) + 1

        if self.ascending:
            for limit in limits:
                if value < limit:
                    return
                self.category -= 1

        else:
            for limit in limits:
                if value > limit:
                    return
                self.category -= 1


@dataclass
class PropertyBase:
    """Class to handle basic compost properties."""

    identity: Identity
    valid_range: Limits
    compliance_range: Limits

    @property
    def compliance(self) -> bool:
        """Property to check if a value is within a specified range."""

        value = self.identity.value
        return self.compliance_range.is_compliant(value)

    def __post_init__(self):
        """Post init method to handle derived properties."""

        self.valid_range.validate(self.identity)


@dataclass
class BasicProperty(PropertyBase):
    """Class to handle basic compost properties."""


@dataclass
class FertilityProperty(PropertyBase):
    """Class to handle fertility compost properties."""

    fertility: Scores

    def __post_init__(self):
        """Post init method to handle derived properties."""

        super().__post_init__()
        self.fertility.assign_category(self.identity.value)


@dataclass
class CleanProperty(PropertyBase):
    """Class to handle clean compost properties."""

    clean: Scores

    def __post_init__(self):
        """Post init method to handle derived properties."""

        super().__post_init__()
        self.clean.assign_category(self.identity.value, clean=True)
