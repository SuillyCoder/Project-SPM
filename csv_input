import csv
import os

def read_csv_columns(filename):
    col1 = []
    col2 = []

    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)

        first_row = next(reader)
        try:
            float(first_row[0])
            col1.append(float(first_row[0]))
            col2.append(float(first_row[1]))
        except ValueError:
            pass

        for row in reader:
            col1.append(float(row[0]))
            col2.append(float(row[1]))

    return col1, col2

filename = input("Enter CSV file path [i.e 'c:/Users/Book1.csv']: ").strip()

if not os.path.isfile(filename):
    print("Error: File does not exist")
else:
    array1, array2 = read_csv_columns(filename)
    print("x:", array1)
    print("f(x):", array2)
