
def run():
    import csv
    import psycopg
    def export_to_postgres(data):


        with psycopg.connect("host=postgres_server dbname=dataset "
                             + "user=dataengineer password=dataengineer") as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO covid values(%s, %s, %s, %s)", data)
            conn.commit()

    data = []
    with open("/shared_dir/covid.csv", "r") as f:
        csv_data = csv.reader(f, delimiter=',')
        got_header = False
        for row in csv_data:
            if not got_header:
                got_header = True
                continue
            data.append((row[3], row[7], row[8], row[4][0:10]))
    export_to_postgres(data)
