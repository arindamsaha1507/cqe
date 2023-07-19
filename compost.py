"""Module to compute compost quality grade."""


from enum import Enum

import parameters

from properties import (
    BasicProperty,
    FertilityProperty,
    CleanProperty,
    Identity,
    Limits,
    Scores,
)


class PropertyType(Enum):
    """Enum to represent compost property type."""

    BASIC = "basic"
    FERTILITY = "fertility"
    CLEAN = "clean"


class Compost:
    """Class representing Compost"""

    def __init__(self, inputs: dict[str, float]):
        """Constructor method to initialize compost properties."""

        if "Ratio" in set(inputs.keys()):
            raise ValueError("Ratio should not be specified manually.")

        inputs["Ratio"] = inputs["Carbon"] / inputs["Nitrogen"]

        input_keys = list(inputs.keys())
        parameter_keys = parameters.get_all_property_names()

        if set(input_keys) != set(parameter_keys):
            raise ValueError(f"Expected keys: {parameter_keys}, got: {input_keys}.")

        self.properties: dict[
            PropertyType, dict[str, BasicProperty | FertilityProperty | CleanProperty]
        ] = {
            PropertyType.BASIC: {},
            PropertyType.FERTILITY: {},
            PropertyType.CLEAN: {},
        }

        for name, value in inputs.items():
            identity = Identity(name, value, parameters.units[name])
            valid_range = Limits(*parameters.valid_range[name])
            compliance_range = Limits(*parameters.compliance_range[name])

            if name in parameters.get_fi_property_names():
                fertility = Scores(
                    parameters.fi_weight[name], parameters.fi_class[name]
                )
                self.properties[PropertyType.FERTILITY][name] = FertilityProperty(
                    identity, valid_range, compliance_range, fertility
                )
            elif name in parameters.get_ci_property_names():
                clean = Scores(parameters.ci_weight[name], parameters.ci_class[name])
                self.properties[PropertyType.CLEAN][name] = CleanProperty(
                    identity, valid_range, compliance_range, clean
                )
            else:
                self.properties[PropertyType.BASIC][name] = BasicProperty(
                    identity, valid_range, compliance_range
                )

    def check_compliance(self) -> bool:
        """Method to check if compost is compliant."""

        for property_type in PropertyType:
            for prop in self.properties[property_type].values():
                if not prop.compliance_range.is_compliant(prop.identity.value):
                    return False

        return True

    def get_fertility_index(self) -> float:
        """Method to compute fertility index."""

        num = 0.0
        den = 0.0

        for prop in self.properties[PropertyType.FERTILITY].values():
            num += prop.fertility.category * prop.fertility.weight
            den += prop.fertility.weight

        return num / den

    def get_clean_index(self) -> float:
        """Method to compute fertility index."""

        num = 0.0
        den = 0.0

        for prop in self.properties[PropertyType.CLEAN].values():
            num += prop.clean.category * prop.clean.weight
            den += prop.clean.weight

        return num / den


def main():
    """Main function."""

    inputs = {
        "Moisture Content": 1,
        "pH": 2,
        "Electrical Conductivity": 3.0,
        "Bulk Density": 4,
        "Carbon": 5,
        "Nitrogen": 6,
        "Phosphorous": 7.0,
        "Potassium": 8.0,
        "Zinc": 9.0,
        "Copper": 10.0,
        "Cadmium": 11.0,
        "Lead": 12.0,
        "Chromium": 13.0,
        "Nickel": 14.0,
    }

    compost = Compost(inputs)

    print(compost.check_compliance())
    print(compost.get_fertility_index())
    print(compost.get_clean_index())


if __name__ == "__main__":
    main()
