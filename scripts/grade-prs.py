
import argparse
import csv

import roboyml
from settings import *

from canvasgrades import CanvasGradeFile


def __main__():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'gradefile',
        type=str,
        help="Canvas gradebook csv for modification",
    )

    args = parser.parse_args()

    with CanvasGradeFile(Path(args.gradefile)) as gradebook, roboyml.open(studentfile) as students:
        for idx, graderow in enumerate(gradebook.rows):
            if graderow[canvas_netid_col] not in students.keys():
                print(f"WARN: {graderow[canvas_netid_col]} not in students.yml")
                continue
            student = students[graderow[canvas_netid_col]]
            # print(f">>> Processing {student['name']}")

            if graderow[assignment_student_pr]:
                # ignore grades already set
                continue
            elif pytz.utc.localize(student['student_pr']['merged_at']) > assignment_student_pr_due:
                print(f"{student['name']} / {student['netid']} / {student['github']} has late personal PR")
                graderow[assignment_student_pr] = 0
            else:
                graderow[assignment_student_pr] = gradebook.maxpoints[assignment_student_pr]

    # for r in gradebook.rows:
    #     print(f"{r[canvas_netid_col]}")

if __name__ == "__main__":
    __main__()
