#!/bin/bash

airflow initdb
airflow webserver -p 8080 &
sleep 5s

airflow scheduler &
sleep 5s

airflow users  create --role Admin --username dataengineer --email admin@admin.co --firstname admin --lastname admin --password dataengineer

tail -F /dev/null
