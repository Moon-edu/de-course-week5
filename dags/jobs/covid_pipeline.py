from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonVirtualenvOperator
from datetime import datetime, timedelta

COVID_ENDPOINT_TMPL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                 + f"/csse_covid_19_daily_reports/%s.csv"

OUTPUT_PATH = "/shared_dir/covid.csv"

with DAG('covid',
         start_date=datetime(2022, 10, 1),
         max_active_runs=3,
         catchup=False,
         schedule_interval="0 * * * *") as dag:
    date_to_download = (datetime.today() - timedelta(days=30)).strftime("%m-%d-%Y")

    endpoint = COVID_ENDPOINT_TMPL % date_to_download
    downloader = BashOperator(
        task_id='download',
        bash_command=f'curl -k -o {OUTPUT_PATH} {endpoint}')

    from tasks import covid_exporter

    exporter = PythonVirtualenvOperator(
        task_id='print',
        python_callable=covid_exporter.run,
        requirements=["psycopg==3.1.4"]
    )

    downloader >> exporter
