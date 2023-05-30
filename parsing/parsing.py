import os
from typing import List
import json

import openpyxl
from openpyxl import load_workbook


PATH = os.path.dirname(__file__) + r"\src"


GRADUATE_SCHOOL = 1

JSON_OUT = {}

# DAYS_OF_WEEK = ["ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА"]


def get_files(path: str) -> List:
    files = []

    for filename in os.listdir(path):

        f = os.path.join(path, filename)

        if os.path.isfile(f):
            files.append(f)

    return files


def get_merged_cells(cur_sheet) -> List:
    merged_cells = []

    for merged_cell in cur_sheet.merged_cells.ranges:
        if merged_cell.min_col == 2 and merged_cell.max_col == 2:
            merged_cells.append(merged_cell)

    return merged_cells


for excel_path in get_files(PATH):
    try:
        wb = load_workbook(filename=excel_path)
    except PermissionError as e:
        print("Необходимо закрыть все файлы Excel для корректной работы.")

    quantity_sheets = len(wb.sheetnames)

    if quantity_sheets == GRADUATE_SCHOOL:
        pass
    else:
        for i in range(quantity_sheets - 1):
            sheet = wb.worksheets[i]

            JSON_OUT[sheet.title] = {}

            merged_cells = get_merged_cells(sheet)

            # print(merged_cells[0].bounds)  # (2, 13, 2, 16) == B13:B16

            if merged_cells:
                for day_coord in merged_cells:
                    _, bottom, _, top = day_coord.bounds
                    day_of_week = sheet[bottom][1].value
                    # JSON_OUT[sheet.title] += {
                    #
                    # }
                    delay = top - bottom + 1
                    for i in range(delay):
                        if i % 2 == 0:
                            period = sheet[bottom + i][2].value
                            # JSON_OUT[sheet.title] = {
                            #     day_of_week: {
                            #         period
                            #     }
                            # }
                            for j in range(2):
                                week_parity = sheet[bottom + i + j][3].value
                                subjects = []
                                max_cols = sheet.max_column
                                for k in range(max_cols - 4):
                                    subject = sheet[bottom + i + j][4 + k].value

                                    if subject is None:
                                        continue

                                    subject = subject.replace("\n", " ")
                                    subjects.append(subject)

                                JSON_OUT[sheet.title].update({
                                    day_of_week: {
                                        period: {
                                            week_parity: subjects
                                        }
                                    }
                                })
                                # print(excel_path, sheet.title, day_of_week, period, week_parity, subjects)


with open("data_file.json", "w") as write_file:
    json.dump(JSON_OUT, write_file, ensure_ascii=False)
