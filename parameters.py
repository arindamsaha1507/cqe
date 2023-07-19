"""Constant Parameters for the application"""

units = {
    "Moisture Content": "%",
    "pH": "-",
    "Electrical Conductivity": "dS/m",
    "Bulk Density": "g/cm3",
    "Carbon": "%",
    "Nitrogen": "%",
    "Phosphorous": "%",
    "Potassium": "%",
    "Zinc": "mg/kg",
    "Copper": "mg/kg",
    "Cadmium": "mg/kg",
    "Lead": "mg/kg",
    "Chromium": "mg/kg",
    "Nickel": "mg/kg",
    "Ratio": "-",
}

valid_range = {
    "Moisture Content": (0, 100),
    "pH": (0, 14),
    "Electrical Conductivity": (0, 20),
    "Bulk Density": (0, 5),
    "Carbon": (0, 100),
    "Nitrogen": (0, 100),
    "Phosphorous": (0, 100),
    "Potassium": (0, 100),
    "Zinc": (0, 10000),
    "Copper": (0, 10000),
    "Cadmium": (0, 10000),
    "Lead": (0, 10000),
    "Chromium": (0, 10000),
    "Nickel": (0, 10000),
    "Ratio": (0, 1000000),
}

compliance_range = {
    "Moisture Content": (15, 25),
    "pH": (6.5, 7.5),
    "Electrical Conductivity": (0, 4),
    "Bulk Density": (0, 1),
    "Carbon": (12, 100),
    "Nitrogen": (0.8, 100),
    "Phosphorous": (0.175, 100),
    "Potassium": (0.333, 100),
    "Zinc": (0, 1000),
    "Copper": (0, 300),
    "Cadmium": (0, 5),
    "Lead": (0, 100),
    "Chromium": (0, 50),
    "Nickel": (0, 50),
    "Ratio": (0, 20),
}

fi_weight = {
    "Carbon": 5,
    "Nitrogen": 3,
    "Phosphorous": 3,
    "Potassium": 1,
    "Ratio": 3,
}

ci_weight = {
    "Zinc": 1,
    "Copper": 2,
    "Cadmium": 5,
    "Lead": 3,
    "Chromium": 3,
    "Nickel": 1,
}

fi_class = {
    "Carbon": [20.05, 15.05, 12.05, 9.05],
    "Nitrogen": [1.25, 1.05, 0.805, 0.505],
    "Phosphorous": [0.605, 0.405, 0.205, 0.105],
    "Potassium": [1.049, 0.755, 0.505, 0.255],
    "Ratio": [10.05, 15.05, 20.05, 25.05],
}

ci_class = {
    "Zinc": [150.5, 300.5, 500.5, 700.5, 900.5],
    "Copper": [50.5, 100.5, 200.5, 400.5, 600.5],
    "Cadmium": [0.35, 0.65, 1.05, 2.05, 4.05],
    "Lead": [50.5, 100.5, 150.5, 250.5, 400.5],
    "Chromium": [50.5, 100.5, 150.5, 250.5, 350.5],
    "Nickel": [20.5, 40.5, 80.5, 120.5, 160.5],
}


def validate_parameters():
    """Helper function to validate if keys are proper."""

    if set(units.keys()) != set(valid_range.keys()):
        raise ValueError("Units and valid range should have the same keys.")

    if set(valid_range.keys()) != set(compliance_range.keys()):
        raise ValueError("Valid and compliance range should have the same keys.")

    if set(fi_weight.keys()) != set(fi_class.keys()):
        raise ValueError("FI weight and class should have the same keys.")

    if set(ci_weight.keys()) != set(ci_class.keys()):
        raise ValueError("CI weight and class should have the same keys.")

    if not set(fi_class.keys()).issubset(set(valid_range.keys())):
        raise ValueError("FI class should be a subset of valid range keys.")

    if not set(ci_class.keys()).issubset(set(valid_range.keys())):
        raise ValueError("CI class should be a subset of valid range keys.")

    if not set(fi_class.keys()).isdisjoint(set(ci_class.keys())):
        raise ValueError("FI and CI class should have disjoint keys.")


def get_all_property_names():
    """Helper function to get all property names."""
    return list(valid_range.keys())


def get_fi_property_names():
    """Helper function to get all FI property names."""
    return list(fi_class.keys())


def get_ci_property_names():
    """Helper function to get all CI property names."""
    return list(ci_class.keys())


validate_parameters()
