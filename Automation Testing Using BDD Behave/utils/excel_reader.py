import openpyxl
import os

def get_excel_data(file_name, sheet_name=None):
    data = []
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", file_name)
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name] if sheet_name else workbook.active
    
    headers = [cell.value for cell in sheet[1]]
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = dict(zip(headers, row))
        data.append(row_data)
    return data
