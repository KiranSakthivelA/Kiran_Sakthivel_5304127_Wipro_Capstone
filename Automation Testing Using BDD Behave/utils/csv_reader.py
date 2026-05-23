import csv
import os

def get_csv_data(file_name):
    data = []
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", file_name)
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data
