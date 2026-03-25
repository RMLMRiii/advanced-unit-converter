import csv

HISTORY_FILE = "conversion_history.csv"


def display_history() -> None:
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)

            if len(rows) <= 1:
                print("No conversion history found.")
                return

            print("\nCONVERSION HISTORY")
            print("-" * 80)

            for row in rows:
                print(" | ".join(row))

    except FileNotFoundError:
        print("History file not found.")
    except OSError as error:
        print(f"Error reading history file: {error}")


if __name__ == "__main__":
    display_history()
