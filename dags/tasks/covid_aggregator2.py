
def run(datadate):
    import psycopg
    from datetime import datetime
    from airflow.hooks.base_hook import BaseHook

    datadate = datetime.strptime(datadate, '%Y-%m-%d')
    print(f"Aggregating data in {datadate}")

    def get_covid_stat_postgres():
        conn_info = BaseHook.get_connection("job_postgres")
        with psycopg.connect(f"host={conn_info.host} dbname=dataset "
                             + f"user={conn_info.login} password={conn_info.password}") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        country, acc_confirmed, death
                    FROM 
                        covid 
                    WHERE
                        datadate = %s
                """, (datadate, ))
                return cur.fetchall()

    def get_total_confirmed(data):
        sum = 0
        for d in data:
            sum += d[1]
        return sum

    def get_avg_confirmed(data, sum):
        return sum / len(data)

    def get_country_of_max_confirmed(data):
        max = -1
        country = None
        for d in data:
            if max < d[1]:
                max = d[1]
                country = d[0]
        return country

    def get_country_of_max_death_rate(data):
        max = 0
        country = None
        for d in data:
            if d[1] > 0 and max < (d[2] / d[1] * 100):
                max = d[2] / d[1] * 100
                country = d[0]
        return country

    all_covid_data = get_covid_stat_postgres()
    if len(all_covid_data) == 0:
        print("No Data!")
        return

    total_confirmed = get_total_confirmed(all_covid_data)
    avg_confirmed = get_avg_confirmed(all_covid_data, total_confirmed)
    max_conf_ctr = get_country_of_max_confirmed(all_covid_data)
    max_death_rate_ctr = get_country_of_max_death_rate(all_covid_data)

    print(f"""
        Summary:
          Total confirmed: {total_confirmed}
          World average confirmed: {avg_confirmed}
          Max confirmed country: {max_conf_ctr}
          Max death rate country: {max_death_rate_ctr}
    """)
