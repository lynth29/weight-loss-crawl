import csv


def save_csv(input_data: list, output_path: str):
    fieldnames = [
        "day",
        "title",
        "short_title",
        "workout_length",
        "workout_types",
        "secondary_types",
        "url",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in input_data:
            writer.writerow(row)