from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonVirtualenvOperator
from datetime import datetime
from tasks import covid_exporter1


with DAG('covid',
         start_date=datetime(2022, 11, 3),
         schedule_interval="0 0 * * *",
         catchup=True) as dag:

    COVID_ENDPOINT = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                          + f"/csse_covid_19_daily_reports/10-01-2022.csv"

    OUTPUT_PATH = "/shared_dir/covid.csv"

    downloader = BashOperator(
        task_id='download',
        bash_command=f'curl -k -o {OUTPUT_PATH} '
                     + f'{COVID_ENDPOINT}')

    exporter = PythonVirtualenvOperator(
        task_id='export',
        python_callable=covid_exporter1.run,
        requirements=["psycopg==3.1.4"]
    )

    downloader >> exporter
