
def run(datadate):
    import csv
    import psycopg
    from datetime import datetime
    def export_to_postgres(data):
        with psycopg.connect(f"host=postgres.server.local dbname=dataset "
                             + f"user=dataengineer password=dataengineer") as conn:
            with conn.cursor() as cur:
                cur.executemany("INSERT INTO covid values(%s, %s, %s, %s, %s, %s)", data)
            conn.commit()

    data = []

    with open(f"/shared_dir/covid-{datadate}.csv", "r") as f:
        csv_data = csv.reader(f, delimiter=',')
        got_header = False
        for row in csv_data:
            if not got_header:
                got_header = True
                continue
            confirmed = int(row[7])
            death = int(row[8])
            recovered = int(row[9]) if row[9].strip() else 0
            active = int(row[10]) if row[10].strip() else 0
            datadate = datetime.strptime(row[4][0:10], '%Y-%m-%d')

            data.append((row[3], confirmed, death, recovered, active, datadate))

    export_to_postgres(data)

