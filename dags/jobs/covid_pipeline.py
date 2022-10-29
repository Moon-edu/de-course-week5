from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from tasks import covid_exporter

COVID_ENDPOINT_TMPL = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data" \
                 + f"/csse_covid_19_daily_reports/%s.csv"

OUTPUT_PATH = "/shared_dir/covid.csv"

with DAG('covid',
         start_date=datetime(2022, 10, 1),
         max_active_runs=3,
         schedule_interval="*/10 * * * *") as dag:
    date_to_download = (datetime.today() - timedelta(days=30)).strftime("%m-%d-%Y")

    endpoint = COVID_ENDPOINT_TMPL % date_to_download
    downloader = BashOperator(
        task_id='download',
        bash_command=f'curl -i -k -o {OUTPUT_PATH} {endpoint}')

    printer = PythonOperator(
        task_id='print',
        python_callable=covid_exporter.run
    )