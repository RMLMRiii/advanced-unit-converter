import csv
from datetime import datetime

HISTORY_FILE = "conversion_history.csv"


LENGTH_UNITS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.344,
}

MASS_UNITS = {
    "mg": 0.000001,
    "g": 0.001,
    "kg": 1.0,
    "lb": 0.45359237,
    "oz": 0.028349523125,
}

TEMPERATURE_UNITS = {"c", "f", "k"}


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    value_in_meters = value * LENGTH_UNITS[from_unit]
    return value_in_meters / LENGTH_UNITS[to_unit]


def convert_mass(value: float, from_unit: str, to_unit: str) -> float:
    value_in_kg = value * MASS_UNITS[from_unit]
    return value_in_kg / MASS_UNITS[to_unit]


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit == to_unit:
        return value

    # Convert input to Celsius first
    if from_unit == "c":
        celsius = value
    elif from_unit == "f":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "k":
        celsius = value - 273.15
    else:
        raise ValueError("Unsupported temperature unit.")

    # Convert Celsius to output unit
    if to_unit == "c":
        return celsius
    elif to_unit == "f":
        return (celsius * 9 / 5) + 32
    elif to_unit == "k":
        return celsius + 273.15
    else:
        raise ValueError("Unsupported temperature unit.")


def save_to_history(category: str, value: float, from_unit: str, to_unit: str, result: float) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, category, value, from_unit, to_unit, result]

    try:
        with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(row)
    except OSError as error:
        print(f"Warning: could not save history. {error}")


def print_header() -> None:
    print("\n" + "=" * 50)
    print("ADVANCED UNIT CONVERTER")
    print("=" * 50)
    print("1. Length")
    print("2. Mass")
    print("3. Temperature")
    print("4. Exit")


def get_float(prompt: str) -> float:
    while True:
        user_input = input(prompt).strip()
        try:
            return float(user_input)
        except ValueError:
            print("Invalid number. Please try again.")


def get_unit(prompt: str, valid_units: set[str] | list[str]) -> str:
    valid_set = set(valid_units)
    while True:
        unit = input(prompt).strip().lower()
        if unit in valid_set:
            return unit
        print(f"Invalid unit. Choose from: {', '.join(sorted(valid_set))}")


def handle_length() -> None:
    print("\nAvailable length units:", ", ".join(sorted(LENGTH_UNITS.keys())))
    value = get_float("Enter value: ")
    from_unit = get_unit("Convert from: ", set(LENGTH_UNITS.keys()))
    to_unit = get_unit("Convert to: ", set(LENGTH_UNITS.keys()))

    result = convert_length(value, from_unit, to_unit)
    print(f"\nResult: {value} {from_unit} = {result:.6f} {to_unit}")
    save_to_history("Length", value, from_unit, to_unit, result)


def handle_mass() -> None:
    print("\nAvailable mass units:", ", ".join(sorted(MASS_UNITS.keys())))
    value = get_float("Enter value: ")
    from_unit = get_unit("Convert from: ", set(MASS_UNITS.keys()))
    to_unit = get_unit("Convert to: ", set(MASS_UNITS.keys()))

    result = convert_mass(value, from_unit, to_unit)
    print(f"\nResult: {value} {from_unit} = {result:.6f} {to_unit}")
    save_to_history("Mass", value, from_unit, to_unit, result)


def handle_temperature() -> None:
    print("\nAvailable temperature units: c, f, k")
    value = get_float("Enter value: ")
    from_unit = get_unit("Convert from: ", TEMPERATURE_UNITS)
    to_unit = get_unit("Convert to: ", TEMPERATURE_UNITS)

    result = convert_temperature(value, from_unit, to_unit)
    print(f"\nResult: {value} {from_unit.upper()} = {result:.6f} {to_unit.upper()}")
    save_to_history("Temperature", value, from_unit.upper(), to_unit.upper(), result)


def main() -> None:
    while True:
        print_header()
        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            handle_length()
        elif choice == "2":
            handle_mass()
        elif choice == "3":
            handle_temperature()
        elif choice == "4":
            print("\nGoodbye.")
            break
        else:
            print("\nInvalid selection. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
