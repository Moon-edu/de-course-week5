def run(datadate):
    import csv
    import xmltodict
    import json
    import psycopg2
    from psycopg2.extras import execute_batch

    # postgres로 export하는 함수 설정 (execute_many -> execute로 변경)
    def export_to_postgres(data):
        with psycopg2.connect(f"host=postgres-hw dbname=stock "
                             + f"user=stock-importer password=stock") as conn:
            with conn.cursor() as cur:
                psycopg2.extras.execute_batch(cur, "INSERT INTO stock VALUES (%s, %s, %s, %s, %s)", data)

            conn.commit()

    # code
    with open(f"/shared_dir/code.csv", "r") as f:
        code_csv = csv.reader(f, delimiter=',')
        header = False
        code_data = []
        for row in code_csv:
            if not header:
                header = True
                continue
            code_data.append(row)
    codes = dict(code_data)

    # category
    with open(f"/shared_dir/category.xml", "r") as f:
        category_xml = xmltodict.parse(f.read())['categories']['category']
    cate = {row['code']: row['name'] for row in category_xml}

    with open(f"/shared_dir/price_{datadate}.json", "r") as f:
        price_json = json.load(f)

    price_data = []

    # 공통 key인 'code'로 코드, 카테고리 테이블에 있는 주식명, 주식 카테고리 value도 함께 가져옴
    for row in price_json:
        price_data.append(
            (row['code'],
             codes[row['code']],
             int(row['price']),
             datadate,
             cate[row['code']])
        )

    export_to_postgres(price_data)