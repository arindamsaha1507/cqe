"""Module for running the compost class."""

from dataclasses import dataclass, field
import yaml

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

    show_compliance: bool
    use_compliance: bool

    @property
    def is_compliant(self) -> bool:
        """Check if the property is compliant with the limits."""

        return self.compliance_limit.min <= self.value <= self.compliance_limit.max

    def __repr__(self) -> str:
        return f"{self.name}: {self.value}, {self.is_compliant}"


@dataclass
class NutritionalProperty(Property):
    """Class for a nutritional property of the compost."""

    fertilization_index: Index

    def __post_init__(self):

        if self.fertilization_index.typ != IndexType.FERTILITY:
            raise ValueError(
                f"Fertilization index of {self.name} must be of type FERTILITY."
            )

        if len(self.fertilization_index.category_limits) != 4:
            raise ValueError(
                f"Fertilization index of {self.name} must have 4 category limits."
            )

        self.set_score()

    def set_score(self):
        """Set the score of the fertilization index based on the value of the property."""

        self.fertilization_index.set_score(self.value)

    def __repr__(self) -> str:
        return f"{self.name}: {self.value}, {self.is_compliant}, {self.fertilization_index.score}"


@dataclass
class HeavyMetalProperty(Property):
    """Class for a heavy metal property of the compost."""

    clean_index: Index

    def __post_init__(self):

        if self.clean_index.typ != IndexType.CLEAN:
            raise ValueError(f"Clean index of {self.name} must be of type CLEAN.")

        if len(self.clean_index.category_limits) != 5:
            raise ValueError(f"Clean index of {self.name} must have 5 category limits.")

        self.set_score()

    def set_score(self):
        """Set the score of the clean index based on the value of the property."""

        self.clean_index.set_score(self.value)

    def __repr__(self) -> str:
        return (
            f"{self.name}: {self.value}, {self.is_compliant}, {self.clean_index.score}"
        )


@dataclass
class CompostProperties:
    """Class for the properties of the compost."""

    moisture: Property
    ph: Property
    conductivity: Property
    bulk_density: Property

    def __repr__(self) -> str:
        return f"\nCompost Properties\n{self.moisture}\n{self.ph}\n{self.conductivity}\n{self.bulk_density}\n"


@dataclass
class CompostNutritionalProperties:
    """Class for the nutritional properties of the compost."""

    organic_matter: NutritionalProperty
    nitrogen: NutritionalProperty
    phosphorus: NutritionalProperty
    potassium: NutritionalProperty

    def __repr__(self) -> str:
        return f"\nCompost Nutritional Properties\n{self.organic_matter}\n{self.nitrogen}\n{self.phosphorus}\n{self.potassium}\n"


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

    def __repr__(self) -> str:
        return f"\nCompost Heavy Metal Properties\n{self.zinc}\n{self.copper}\n{self.cadmium}\n{self.lead}\n{self.chromium}\n{self.nickel}\n{self.arsenic}\n{self.mercury}\n"


@dataclass
class CompostDerivedProperties:
    """Class for the derived properties of the compost."""

    cn_ratio: NutritionalProperty
    npk_ratio: Property

    def __repr__(self) -> str:
        return f"\nCompost Derived Properties\n{self.cn_ratio}\n{self.npk_ratio}\n"


@dataclass
class Compost:
    """Class for the compost."""

    properties: CompostProperties
    nutritional_properties: CompostNutritionalProperties
    heavy_metal_properties: CompostHeavyMetalProperties
    derived_properties: CompostDerivedProperties


class CompostFactory:
    """Factory class for creating compost objects."""

    @staticmethod
    def read_yaml(file_path: str) -> dict:
        """Read a yaml file and return a dictionary."""

        with open(file_path, "r", encoding="utf_8") as file:
            return yaml.safe_load(file)

    @staticmethod
    def create_property(name: str, config: dict, inputs: dict) -> Property:
        """Create a property object from a yaml dictionary."""

        value = inputs[name]
        compliance_limit = Limit(
            config[name]["compliance_limit"][0],
            config[name]["compliance_limit"][1],
        )

        return Property(name, value, Limit(), compliance_limit, True, True)

    @staticmethod
    def create_nutritional_property(
        name: str, config: dict, inputs: dict
    ) -> NutritionalProperty:
        """Create a nutritional property object from a yaml dictionary."""

        value = inputs[name]
        compliance_limit = Limit(
            config[name]["compliance_limit"][0],
            config[name]["compliance_limit"][1],
        )

        return NutritionalProperty(
            name,
            value,
            Limit(),
            compliance_limit,
            True,
            True,
            Index(
                typ=IndexType.FERTILITY,
                weight=config[name]["weight"],
                category_limits=config[name]["category_limits"],
            ),
        )

    @staticmethod
    def create_heavy_metal_property(
        name: str, config: dict, inputs: dict
    ) -> HeavyMetalProperty:
        """Create a heavy metal property object from a yaml dictionary."""

        value = inputs[name]
        compliance_limit = Limit(
            config[name]["compliance_limit"][0],
            config[name]["compliance_limit"][1],
        )

        return HeavyMetalProperty(
            name,
            value,
            Limit(),
            compliance_limit,
            True,
            True,
            Index(
                typ=IndexType.CLEAN,
                weight=config[name]["weight"],
                category_limits=config[name]["category_limits"],
            ),
        )

    @staticmethod
    def create_derived_property(name: str, config: dict, inputs: dict) -> Property:
        """Create a derived property object from a yaml dictionary."""

        compliance_limit = Limit(
            config[name]["compliance_limit"][0],
            config[name]["compliance_limit"][1],
        )

        if name == "cn_ratio":
            value = inputs["organic_matter"] / inputs["nitrogen"]
            return NutritionalProperty(
                name,
                value,
                Limit(),
                compliance_limit,
                True,
                True,
                Index(
                    typ=IndexType.FERTILITY,
                    weight=config[name]["weight"],
                    category_limits=config[name]["category_limits"],
                ),
            )

        if name == "npk":
            value = (
                inputs["nitrogen"]
                + 2.29 * inputs["phosphorus"]
                + 1.21 * inputs["potassium"]
            )
            return Property(name, value, Limit(), compliance_limit, True, True)

        raise ValueError(f"Derived property {name} not recognised.")

    @staticmethod
    def create_from_yaml(configs: dict, inputs: dict) -> Compost:
        """Create a compost object from a yaml dictionary."""

        moisture = CompostFactory.create_property("moisture", configs, inputs)
        ph = CompostFactory.create_property("ph", configs, inputs)
        conductivity = CompostFactory.create_property("conductivity", configs, inputs)
        bulk_density = CompostFactory.create_property("bulk_density", configs, inputs)

        properties = CompostProperties(moisture, ph, conductivity, bulk_density)

        organic_matter = CompostFactory.create_nutritional_property(
            "organic_matter", configs, inputs
        )
        nitrogen = CompostFactory.create_nutritional_property(
            "nitrogen", configs, inputs
        )
        phosphorus = CompostFactory.create_nutritional_property(
            "phosphorus", configs, inputs
        )
        potassium = CompostFactory.create_nutritional_property(
            "potassium", configs, inputs
        )

        nutritional_properties = CompostNutritionalProperties(
            organic_matter, nitrogen, phosphorus, potassium
        )

        zinc = CompostFactory.create_heavy_metal_property("zinc", configs, inputs)
        copper = CompostFactory.create_heavy_metal_property("copper", configs, inputs)
        cadmium = CompostFactory.create_heavy_metal_property("cadmium", configs, inputs)
        lead = CompostFactory.create_heavy_metal_property("lead", configs, inputs)
        chromium = CompostFactory.create_heavy_metal_property(
            "chromium", configs, inputs
        )
        nickel = CompostFactory.create_heavy_metal_property("nickel", configs, inputs)
        arsenic = CompostFactory.create_heavy_metal_property("arsenic", configs, inputs)
        mercury = CompostFactory.create_heavy_metal_property("mercury", configs, inputs)

        heavy_metal_properties = CompostHeavyMetalProperties(
            zinc, copper, cadmium, lead, chromium, nickel, arsenic, mercury
        )

        cn_ratio = CompostFactory.create_derived_property("cn_ratio", configs, inputs)
        npk_ratio = CompostFactory.create_derived_property("npk", configs, inputs)

        derived_properties = CompostDerivedProperties(cn_ratio, npk_ratio)

        print(properties)
        print(nutritional_properties)
        print(heavy_metal_properties)
        print(derived_properties)

        return Compost(properties, nutritional_properties, heavy_metal_properties, derived_properties)

if __name__ == "__main__":

    con = {"moisture": {"compliance_limit": [15, 25]}}

    inp = {"moisture": 20}

    print(CompostFactory.create_property("moisture", con, inp))

    ##################################

    con = CompostFactory.read_yaml("cqe/configs.yml")
    inp = CompostFactory.read_yaml("cqe/inputs.yml")

    CompostFactory.create_from_yaml(con, inp)
