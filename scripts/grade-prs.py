
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
                pass
            elif pytz.utc.localize(student['student_pr']['merged_at']) > assignment_student_pr_due:
                print(f"{student['name']} / {student['netid']} / {student['github']} has late personal PR")
                graderow[assignment_student_pr] = 0
            else:
                graderow[assignment_student_pr] = gradebook.maxpoints[assignment_student_pr]

            if graderow[assignment_team_pr]:
                # ignore grades already set
                pass
            elif student['team_pr']['merged'] == True:
                graderow[assignment_team_pr] = gradebook.maxpoints[assignment_team_pr]
            else:
                graderow[assignment_team_pr] = 0
                print(f"{student['name']} / {student['netid']} / {student['github']} did not merge a team PR")

    # for r in gradebook.rows:
    #     print(f"{r[canvas_netid_col]}")

if __name__ == "__main__":
    __main__()
