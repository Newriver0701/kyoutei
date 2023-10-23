import csv
import math

def find_non_finite_values(file_path):
    non_finite_values = []

    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            for value in row:
                if not math.isfinite(float(value)):
                    non_finite_values.append(value)

    return non_finite_values

# 使用例
file_path = 'data.csv'
non_finite_values = find_non_finite_values(file_path)
print(non_finite_values)
