from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonVirtualenvOperator
from datetime import datetime
from tasks import covid_exporter2
from tasks import covid_aggregator

with DAG('covid3',
         start_date=datetime(2022, 11, 3),
         schedule_interval="0 0 * * *",
         catchup=True) as dag:
    COVID_ENDPOINT_TMPL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                          + f"/csse_covid_19_daily_reports/%s.csv"

    OUTPUT_PATH = "/shared_dir/covid-%s.csv"
    val = "{{ ds }}"
    downloader = BashOperator(
        task_id='download',
        bash_command=f'curl -k -o {OUTPUT_PATH % "{{ ds }}"} '
                     + f'{COVID_ENDPOINT_TMPL % """{{ macros.ds_format(ds, "%Y-%m-%d", "%m-%d-%Y") }}"""}')

    exporter = PythonVirtualenvOperator(
        task_id='export',
        python_callable=covid_exporter2.run,
        requirements=["psycopg==3.1.4"],
        op_args=['{{ ds }}']
    )

    aggregator = PythonVirtualenvOperator(
        task_id='aggregate',
        python_callable=covid_aggregator.run,
        requirements=["psycopg==3.1.4"],
        op_args=['{{ ds }}']
    )

    downloader >> exporter >> aggregator
