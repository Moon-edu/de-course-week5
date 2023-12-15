from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonVirtualenvOperator
from datetime import datetime

def run_save_postgres(date, CSV_OUTPUT_PATH, XML_OUTPUT_PATH, JSON_OUTPUT_PATH_TMPL):
    import psycopg2 as psycopg
    from psycopg2.extras import execute_values
    import csv
    import xmltodict
    import json

    def senddata_postgres(list_stock_data):
        with psycopg.connect(f"host=postgres-hw dbname=stock user=stock-importer password=stock") as conn:
            with conn.cursor() as cur:
                execute_values(cur, f"""
                    insert into stock(code, name, price, price_date, category) values %s;
                """, list_stock_data, page_size=100000)
            conn.commit()

    list_stock_data = [] # [0: code, 1: company, 2: price, 3: date, 4: category]
    stock_code_company = {} # {[0: code, 1: company]}
    stock_code_category = {} # {[0: code, 1: category]}

    with open(CSV_OUTPUT_PATH, "r", encoding="utf-8") as f:
        csv_reader = csv.reader(f, delimiter=',')
        header = dict((data, idx) for idx, data in enumerate(next(csv_reader)))
        for code, company in csv_reader:
            stock_code_company[code] = company

    with open(XML_OUTPUT_PATH, "r", encoding="utf-8") as f:
        xml_dict_list = xmltodict.parse(f.read())['categories']['category']

        for xml_dict in xml_dict_list:
            stock_code_category[xml_dict['code']] = xml_dict['name']

    with open(JSON_OUTPUT_PATH_TMPL % date, "r", encoding="utf-8") as f:
        json_dict_list = json.load(f)
        for json_dict in json_dict_list:
            list_stock_data.append((json_dict['code'], stock_code_company[json_dict['code']], int(json_dict['price']), date, stock_code_category[json_dict['code']]))

    senddata_postgres(list_stock_data)

with DAG('stock',
        start_date=datetime(2021,1,1),
        schedule_interval='0 0 * * *',
        end_date=datetime(2021,1,31),
        catchup=True
        ) as dag:

    CSV_ENDPOINT = "https://raw.githubusercontent.com/Moon-edu/dataset/main/csv/stock/code.csv"
    CSV_OUTPUT_PATH = "/shared_dir/stock_code_company.csv"

    XML_ENDPOINT = "https://raw.githubusercontent.com/Moon-edu/dataset/main/xml/stock/category.xml"
    XML_OUTPUT_PATH = "/shared_dir/stock_code_category.xml"

    JSON_ENDPOINT_TMPL = "https://raw.githubusercontent.com/Moon-edu/dataset/main/json/stock/price-%s.json"
    JSON_OUTPUT_PATH_TMPL = "/shared_dir/stock_code_price_%s.json"

    csv_downloader = BashOperator(
        task_id='download_csv',
        bash_command=f'curl -k -o {CSV_OUTPUT_PATH} {CSV_ENDPOINT}')

    xml_downloader = BashOperator(
        task_id='download_xml',
        bash_command=f'curl -k -o {XML_OUTPUT_PATH} {XML_ENDPOINT}')

    json_downloader = BashOperator(
        task_id='download_json',
        bash_command=f'curl -k -o {JSON_OUTPUT_PATH_TMPL % "{{ ds }}"} {JSON_ENDPOINT_TMPL % "{{ ds }}"}')

    db_saver = PythonVirtualenvOperator(
        task_id='db_save',
        python_callable=run_save_postgres,
        op_args=['{{ ds }}', CSV_OUTPUT_PATH, XML_OUTPUT_PATH, JSON_OUTPUT_PATH_TMPL],
        requirements=["psycopg2==2.9.1", "xmltodict==0.13.0"]
    )
    csv_downloader >> xml_downloader >> json_downloader >> db_saver


