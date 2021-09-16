
from contextlib import contextmanager
import csv
from pathlib import Path


class CanvasGradeFile():
    def __init__(self, file: Path):
        self.file = file

    def __enter__(self):
        with self.file.open('r') as f:
            self.reader = csv.DictReader(f)
            self.rows = list([r for r in self.reader])
            self.fieldnames = self.reader.fieldnames

        print(f"Gradebook loading assignments ...")
        self.assignments = {}
        self.maxpoints = {}
        for i, (assignment, points) in enumerate(self.rows[0].items()):
            print(f"{i}: {points} points, \"{assignment}\"")
            self.assignments[assignment] = i
            self.maxpoints[assignment] = points

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        with self.file.open('w') as f:
            writer = csv.DictWriter(f, self.fieldnames)
            writer.writeheader()
            for r in self.rows:
                writer.writerow(r)

# def load(file: Path):
#     with file.open('r') as f:
#         data = yaml.safe_load(f)
#     return data
#
# def save(file: Path, data):
#     with file.open('w') as f:
#         yaml.dump(data, f)

# @contextmanager
# def open(file: Path):
#     try:
#         if not file.exists():
#             file.touch()
#         data = load(file)
#         yield data
#     finally:
#         save(file, data)
