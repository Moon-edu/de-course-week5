from airflow import DAG
from datetime import datetime
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonVirtualenvOperator
import stock_export

with DAG('stock',
         start_date=datetime(2021, 1, 1),
         end_date=datetime(2021, 1, 31),
         schedule_interval='0 0 * * *',
         catchup=True) as dag:

    # input 데이터 변수
    CODE_INPUT = f"https://raw.githubusercontent.com/Moon-edu/dataset/main/csv/stock/code.csv"
    PRICE_INPUT = f"https://raw.githubusercontent.com/Moon-edu/dataset/main/json/stock/price-%s.json"
    CATEGORY_INPUT = f"https://raw.githubusercontent.com/Moon-edu/dataset/main/xml/stock/category.xml"

    # output 경로 변수
    CODE_OUTPUT = f"/shared_dir/code.csv"
    PRICE_OUTPUT = f"/shared_dir/price_%s.json"
    CATEGORY_OUTPUT = f"/shared_dir/category.xml"

    # price 날짜 변동
    val = "{{ ds }}"

    # 파일 다운로드 오퍼레이터_code, category, price 각각 실행
    download_code = BashOperator(
        task_id='download_code',
        bash_command=f'curl -k -o {CODE_OUTPUT} {CODE_INPUT}'
    )

    download_category = BashOperator(
        task_id='download_category',
        bash_command=f'curl -k -o {CATEGORY_OUTPUT} {CATEGORY_INPUT}'
    )

    download_price = BashOperator(
        task_id='download_price',
        bash_command=f'curl -k -o {PRICE_OUTPUT % "{{ ds }}"} {PRICE_INPUT % "{{ ds }}"}'
    )

    export = PythonVirtualenvOperator(
        task_id='export',
        python_callable=stock_export.run,
        requirements=["psycopg==3.1.4", "xmltodict==0.13.0"],
        op_args=["{{ ds }}"]
    )

    # 의존성 설정 (독립적인 앞의 세 개는 병렬로, export는 3개 작업 이후 실행)
    [download_code, download_category, download_price] >> export