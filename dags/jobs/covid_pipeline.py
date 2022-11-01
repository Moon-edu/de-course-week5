from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonVirtualenvOperator
from datetime import datetime

with DAG('covid',
         start_date=datetime(2022, 10, 1),
         max_active_runs=3,
         catchup=True,
         schedule_interval="0 0 * * *") as dag:
    COVID_ENDPOINT_TMPL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                          + f"/csse_covid_19_daily_reports/%s.csv"

    OUTPUT_PATH = "/shared_dir/covid-%s.csv"

    downloader = BashOperator(
        task_id='download',
        bash_command=f'curl -k -o {OUTPUT_PATH % "{{ ds }}"} '
                     + f'{COVID_ENDPOINT_TMPL % """{{ macros.ds_format(ds, "%Y-%m-%d", "%m-%d-%Y") }}"""}')

    from tasks import covid_exporter
    from tasks import covid_aggregator

    exporter = PythonVirtualenvOperator(
        task_id='export',
        python_callable=covid_exporter.run,
        requirements=["psycopg==3.1.4"],
        op_args=['{{ ds }}']
    )

    aggregator = PythonVirtualenvOperator(
        task_id='aggregator',
        python_callable=covid_aggregator.run,
        requirements=["psycopg==3.1.4"],
        op_args=['{{ ds }}']
    )

    downloader >> exporter >> aggregator
