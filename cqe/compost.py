"""Module for running the compost class."""

from dataclasses import dataclass, field

from cqe.globs import IndexType
from cqe.index import Index


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


@dataclass
class NutritionalProperty(Property):
    """Class for a nutritional property of the compost."""

    fertilization_index: Index

    def __post_init__(self):

        if self.fertilization_index.typ == IndexType.FERTILITY:
            raise ValueError(
                f"Fertilization index of {self.name} must be of type FERTILITY."
            )

        if len(self.fertilization_index.category_limits) != 4:
            raise ValueError(
                f"Fertilization index of {self.name} must have 4 category limits."
            )


@dataclass
class HeavyMetalProperty(Property):
    """Class for a heavy metal property of the compost."""

    clean_index: Index

    def __post_init__(self):

        if self.clean_index.typ == IndexType.CLEAN:
            raise ValueError(f"Clean index of {self.name} must be of type CLEAN.")

        if len(self.clean_index.category_limits) != 5:
            raise ValueError(f"Clean index of {self.name} must have 5 category limits.")


@dataclass
class CompostProperties:
    """Class for the properties of the compost."""

    moisture: Property
    ph: Property
    conductivity: Property
    bulk_density: Property


@dataclass
class CompostNutritionalProperties:
    """Class for the nutritional properties of the compost."""

    organic_matter: NutritionalProperty
    nitrogen: NutritionalProperty
    phosphorus: NutritionalProperty
    potassium: NutritionalProperty


@dataclass
class CompostHeavyMetalProperties:
    """Class for the heavy metal properties of the compost."""

    zinc: HeavyMetalProperty
    copper: HeavyMetalProperty
    cadmium: HeavyMetalProperty
    lead: HeavyMetalProperty
    chromium: HeavyMetalProperty
    nickel: HeavyMetalProperty
    arsenic: HeavyMetalProperty
    mercury: HeavyMetalProperty


@dataclass
class CompostDerivedProperties:
    """Class for the derived properties of the compost."""

    cn_ratio: NutritionalProperty
    npk_ratio: NutritionalProperty


@dataclass
class Compost:
    """Class for the compost."""

    properties: CompostProperties
    nutritional_properties: CompostNutritionalProperties
    heavy_metal_properties: CompostHeavyMetalProperties
    derived_properties: CompostDerivedProperties
