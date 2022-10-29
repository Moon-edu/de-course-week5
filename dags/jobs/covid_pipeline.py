from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

COVID_ENDPOINT_TMPL = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data" \
                 + f"/csse_covid_19_daily_reports/%s.csv"

OUTPUT_PATH = "/shared_dir/covid.csv"

with DAG('covid',
         start_date=datetime(2022, 10, 1),
         max_active_runs=3,
         schedule_interval="10/* * * * *") as dag:
    date_to_download = (datetime.today() - timedelta(days=30)).strftime("%m-%d-%Y")

    endpoint = COVID_ENDPOINT_TMPL % date_to_download
    t2 = BashOperator(
        task_id='download',
        bash_command=f'curl -i -k -o {OUTPUT_PATH} {endpoint}')
