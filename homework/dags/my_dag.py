from airflow import DAG
from datetime import datetime

# Database 정보
# host: localhost
# dbname: stock
# user: stock-importer
# passsword: stock

# target table information
# create table stock(
# 	code varchar(10) not null,
# 	name varchar(10) not null,
# 	price int not null,
# 	price_date varchar(15) not null,
# 	category varchar(30) not null
# )


with DAG('stock',
         start_date=datetime(2021, 1, 1),
         schedule_interval="0 0 * * *",
         catchup=True) as dag:

    price_downloader = ...
    category_downloader = ...
    code_downloader = ...

    processor = ...

    exporter = ...

    x >> y >> z
