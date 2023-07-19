"""Module for running the compost class."""

from cqe import Compost


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
    print(compost.get_grade())


if __name__ == "__main__":
    main()
