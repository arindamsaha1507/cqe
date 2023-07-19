"""Module to compute compost quality grade."""


from enum import Enum

from cqe import parameters

from cqe.properties import (
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

        num = sum(
            prop.fertility.category * prop.fertility.weight
            for prop in self.properties[PropertyType.FERTILITY].values()
        )

        den = sum(
            prop.fertility.weight
            for prop in self.properties[PropertyType.FERTILITY].values()
        )

        return num / den

    def get_clean_index(self) -> float:
        """Method to compute fertility index."""

        num = sum(
            prop.clean.category * prop.clean.weight
            for prop in self.properties[PropertyType.CLEAN].values()
        )
        den = sum(
            prop.clean.weight for prop in self.properties[PropertyType.CLEAN].values()
        )

        return num / den
