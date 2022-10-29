import csv


def run():
    header = None
    data = []
    with open("/shared_dir/covid.csv", "r") as f:
        csv_data = csv.reader(f, delimiter=',')
        got_header = False
        for row in csv_data:
            if not got_header:
                header = row
                got_header = True
                continue
            print(row[3])