
def run(datadate):
    import csv
    import xmltodict
    import json
    import psycopg
    from datetime import datetime
    from airflow.hooks.base_hook import BaseHook
    
    
    def export_to_postgres(data):
        with psycopg.connect(f"host=postgres-hw dbname=stock "
                             + f"user=stock-importer password=stock") as conn:
            with conn.cursor() as cur:
                cur.executemany("INSERT INTO stock values(%s, %s, %s, %s, %s)", data)
            conn.commit()

    data = []
    stock_info = dict()
    header = None
    
    with open("/shared_dir/code.csv", "r") as f:
        csv_data = csv.reader(f, delimiter=",")
        got_header = False
        for row in csv_data:
            if not got_header:
                header = row
                got_header = True
                continue
            code, name = row
            stock_info[code] = name

        
    with open("/shared_dir/category.xml", "r") as f:
        xml_data = xmltodict.parse(f.read())
        
        for d in xml_data['categories']['category']:
            code, category = d['code'], d['name']
            stock_info[code] = (stock_info[code], category)

            
    with open(f"/shared_dir/price-{datadate}.json", "r") as f:
        price_data = json.load(f)
        
        for item in price_data:
            
            code = item['code']
            end_price = item['price']
            name = stock_info[code][0]
            category = stock_info[code][1]

            data.append((code, name, end_price, datadate, category))
            
    export_to_postgres(data)
