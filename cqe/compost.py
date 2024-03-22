"""Module for running the compost class."""

from dataclasses import dataclass, field
from typing import Callable
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


class Properties:
    """Base class for the properties of the compost."""

    def show_all_properties(self) -> str:
        """Show all the properties of the compost."""

        strings = []

        for prop in self.__dict__.values():
            strings.append(str(prop))

        return "\n".join(strings)

    def show_all_properties_with_header(self, header: str) -> str:
        """Show all the properties of the compost with a header."""

        strings = self.show_all_properties().split("\n")
        strings.insert(0, header)

        return "\n" + "\n".join(strings)


@dataclass
class CompostProperties(Properties):
    """Class for the properties of the compost."""

    moisture: Property
    ph: Property
    conductivity: Property
    bulk_density: Property

    def __repr__(self) -> str:
        return self.show_all_properties_with_header("Compost Properties")


@dataclass
class CompostNutritionalProperties(Properties):
    """Class for the nutritional properties of the compost."""

    organic_matter: NutritionalProperty
    nitrogen: NutritionalProperty
    phosphorus: NutritionalProperty
    potassium: NutritionalProperty

    @property
    def fertility_index(self) -> float:
        """Calculate the fertility index of the compost."""

        num = sum(
            prop.fertilization_index.weight * prop.fertilization_index.score
            for prop in self.__dict__.values()
        )
        den = sum(prop.fertilization_index.weight for prop in self.__dict__.values())

        return num / den

    def __repr__(self) -> str:
        return self.show_all_properties_with_header("Compost Nutritional Properties")


@dataclass
class CompostHeavyMetalProperties(Properties):
    """Class for the heavy metal properties of the compost."""

    # pylint: disable=too-many-instance-attributes

    zinc: HeavyMetalProperty
    copper: HeavyMetalProperty
    cadmium: HeavyMetalProperty
    lead: HeavyMetalProperty
    chromium: HeavyMetalProperty
    nickel: HeavyMetalProperty
    arsenic: HeavyMetalProperty
    mercury: HeavyMetalProperty

    @property
    def clean_index(self) -> float:
        """Calculate the clean index of the compost."""

        num = sum(
            prop.clean_index.weight * prop.clean_index.score
            for prop in self.__dict__.values()
        )
        den = sum(prop.clean_index.weight for prop in self.__dict__.values())

        return num / den

    def __repr__(self) -> str:
        return self.show_all_properties_with_header("Compost Heavy Metal Properties")


@dataclass
class CompostDerivedProperties(Properties):
    """Class for the derived properties of the compost."""

    cn_ratio: NutritionalProperty
    npk_ratio: Property

    def __repr__(self) -> str:
        return self.show_all_properties_with_header("Compost Derived Properties")


@dataclass
class Compost:
    """Class for the compost."""

    properties: CompostProperties
    nutritional_properties: CompostNutritionalProperties
    heavy_metal_properties: CompostHeavyMetalProperties
    derived_properties: CompostDerivedProperties

    @property
    def is_compliant(self) -> bool:
        """Check if the compost is compliant with all the limits."""

        all_properties = (
            *vars(self.properties).values(),
            *vars(self.nutritional_properties).values(),
            *vars(self.heavy_metal_properties).values(),
            *vars(self.derived_properties).values(),
        )

        return all(prop.is_compliant for prop in all_properties if prop.use_compliance)


class CompostFactory:
    """Factory class for creating compost objects."""

    @staticmethod
    def read_yaml(file_path: str) -> dict:
        """Read a yaml file and return a dictionary."""

        with open(file_path, "r", encoding="utf_8") as file:
            return yaml.safe_load(file)

    @staticmethod
    def create_limit_from_config(config: dict, name: str) -> Limit:
        """Create a limit object from a yaml dictionary."""

        return Limit(
            config[name]["compliance_limit"][0],
            config[name]["compliance_limit"][1],
        )

    @staticmethod
    def create_index(name: str, typ: IndexType, config: dict) -> Index:
        """Create an index object from a yaml dictionary."""

        return Index(
            typ=typ,
            weight=config[name]["weight"],
            category_limits=config[name]["category_limits"],
        )

    @staticmethod
    def create_property(name: str, config: dict, inputs: dict) -> Property:
        """Create a property object from a yaml dictionary."""

        value = inputs[name]
        compliance_limit = CompostFactory.create_limit_from_config(config, name)

        return Property(name, value, Limit(), compliance_limit, True, True)

    @staticmethod
    def create_nutritional_property(
        name: str, config: dict, inputs: dict
    ) -> NutritionalProperty:
        """Create a nutritional property object from a yaml dictionary."""

        value = inputs[name]
        compliance_limit = CompostFactory.create_limit_from_config(config, name)

        return NutritionalProperty(
            name,
            value,
            Limit(),
            compliance_limit,
            True,
            True,
            CompostFactory.create_index(name, IndexType.FERTILITY, config),
        )

    @staticmethod
    def create_heavy_metal_property(
        name: str, config: dict, inputs: dict
    ) -> HeavyMetalProperty:
        """Create a heavy metal property object from a yaml dictionary."""

        value = inputs[name]
        compliance_limit = CompostFactory.create_limit_from_config(config, name)

        return HeavyMetalProperty(
            name,
            value,
            Limit(),
            compliance_limit,
            True,
            True,
            CompostFactory.create_index(name, IndexType.CLEAN, config),
        )

    @staticmethod
    def npk_calculator(inputs: dict) -> float:
        """Calculate the npk ratio of the compost."""

        nitrogen = inputs["nitrogen"]
        phosphorus = inputs["phosphorus"]
        potassium = inputs["potassium"]

        return nitrogen + 2.29 * phosphorus + 1.21 * potassium

    @staticmethod
    def cn_calculator(inputs: dict) -> float:
        """Calculate the cn ratio of the compost."""

        organic_matter = inputs["organic_matter"]
        nitrogen = inputs["nitrogen"]

        return organic_matter / nitrogen

    @staticmethod
    def function_mapper() -> dict[str, (Callable, Callable)]:
        """Map the derived property name to the function that calculates it."""

        return {
            "cn_ratio": (
                CompostFactory.cn_calculator,
                CompostFactory.create_nutritional_property,
            ),
            "npk": (
                CompostFactory.npk_calculator,
                CompostFactory.create_property,
            ),
        }

    @staticmethod
    def create_derived_property(name: str, config: dict, inputs: dict) -> Property:
        """Create a derived property object from a yaml dictionary."""

        if name not in CompostFactory.function_mapper():
            raise ValueError(f"Derived property {name} not recognised.")

        function_map = CompostFactory.function_mapper()
        calculator, creator = function_map[name]
        value = calculator(inputs)
        return creator(name, config, {name: value})

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

        return Compost(
            properties,
            nutritional_properties,
            heavy_metal_properties,
            derived_properties,
        )


if __name__ == "__main__":

    con = {"moisture": {"compliance_limit": [15, 25]}}

    inp = {"moisture": 20}

    print(CompostFactory.create_property("moisture", con, inp))

    ##################################

    con = CompostFactory.read_yaml("cqe/configs.yml")
    inp = CompostFactory.read_yaml("cqe/inputs.yml")

    compost = CompostFactory.create_from_yaml(con, inp)

    print(compost.nutritional_properties.fertility_index)
    print(compost.heavy_metal_properties.clean_index)
    print(compost.is_compliant)
