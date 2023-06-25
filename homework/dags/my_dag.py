"""
###### 5주차 과제 ######

다음의 링크에 가면 주식 데이터가 있습니다.
1. 종목 코드와 회사명(CSV format) 
https://raw.githubusercontent.com/Moon-edu/dataset/main/csv/stock/code.csv

2. 날짜별 종가(당일 마지막 가격)(JSON format)
https://raw.githubusercontent.com/Moon-edu/dataset/main/json/stock/price-2021-01-01.json
위 url에서 날짜만 바꾸면 다른 날짜의 데이터를 가져올 수 있습니다. 위의 url은 2021-01-01의 종가데이터이며,
만약 2021-01-03의 데이터를 가져오고 싶다면 아래와 같이 날짜 부분만 바꾸면 됩니다.
https://raw.githubusercontent.com/Moon-edu/dataset/main/json/stock/price-2021-01-03.json
날짜는 2021-01-01 ~ 2021-01-31일까지의 데이터만 사용할 예정이므로, 1월 31일까지의 데이터만 가져오는 파이프라인을 작성해야합니다.

3. 종목코드별 카테고리(e.g 삼성전자: 전자제품)(XML format)
각 종목 코드는 1개의 카테고리에 1대 1로 매핑됩니다. 예를 들면 삼성전자는 전자제품 카테고리에만 있으며, 삼성전자가 전자제품+소프트웨어라는 복수의 카테고리로
묶여있지 않습니다.
아래의 주소로 접근하면 종목 코드별 카테고리 정보를 담고 있는 xml데이터를 가져올 수 있습니다.
https://raw.githubusercontent.com/Moon-edu/dataset/main/xml/stock/category.xml

여러분이 구성해야 할 데이터 파이프라인은 위의 안내사항에서 제시된 데이터를 엮어 하나의 Postgres table로 데이터를 전달하는 것입니다.
최종 데이터 종착지인 Postgres 테이블의 정의는 아래와 같습니다.
    create table stock(
        code char(6) not null,
        name varchar(10) not null,
        price int not null,
        price_date timestamp not null,
        category varchar(30) not null
    )

위의 테이블 정의를 잘 보시면, 제시된 3개의 데이터가 모두 엮여서 하나의 테이블을 구성함을 알 수 있습니다. stock테이블의 레코드 구성의 예는 아래와 같습니다.
('A10000', '삼성전자', 85000, '2022-05-07', '전자제품')
('A10000', '삼성전자', 83000, '2022-05-08', '전자제품')
('A10000', '삼성전자', 90000, '2022-05-09', '전자제품')
...
접속해야할 Database의 정보는 아래와 같습니다.
host: postgres-hw(debugging을 위해 여러분의 DB client-DBeaver에서 접근시 localhost를 사용하세요)
dbname: stock
user: stock-importer
passsword: stock

****************** 여기서부터 여러분이 구현해야할 파이프라인의 요구사항입니다. **********************************
1. 여러분은 DAG을 구현해야 하며, DAG의 이름은 stock입니다.
2. DAG의 시작일은 종가데이터의 시작일인 2021-01-01이며, (Hint: start_date를 설정해야합니다.)
3. DAG의 시작일은 2022-01-31이며(1달치), (Hint: end_date를 설정해야합니다.)
4. 데이터가 일단위 데이터이기 때문에 매일 0시에 Pipeline이 시작되도록 DAG을 구성해야합니다. (Hint: schedule_interval 옵션을 설정해야 합니다.)
5. Airflow가 파이프라인을 실행했을 때 못다한 과거 데이터 처리를 하도록 설정을 하셔야합니다.(Hint: catchup 옵션을 설정해야 합니다.)
6. 파이프라인의 구성은 여러분의 몫이며, 어떻게 구성하든 Postgres DB에 있는 stock테이블에 정확한 데이터가 있다면 모두 100점입니다. 그러나, 가장 효율적
으로 파이프라인을 구성해보도록 고민해보세요. 예를 들면, 몇 개의 Operator로 나누고 어떤 것은 병렬로, 어떤 것은 직렬로 구성할 것인지 등등. 각 Operator는 
가능한한 Simple 할수록 테스트하기도 좋고, 유지보수하기가 쉬워진다는 점을 생각해보시기 바랍니다.
7. 앞서 설명한 데이터에 접근하기 위해서는 http(https)를 통해 접근해야 한다는 점입니다. 실습에서 우리는 BashOperator를 이용했었다는 점을 기억하세요.
**************************************************************************************************

여러분이 구현한 과제를 테스트해보기 위해서는 아래의 절차를 따르세요.
# docker로 airflow를 실행합니다.
$ docker compose -f docker-compose-hw.yml up

조금 기다리신 후 크롬 등의 웹브라우저를 켠 후 localhost:8080에 접속하면 airflow에 접근할 수 있습니다.
실습때와 같이 로그인 한 후(id: dataengineer, password: dataengineer) 여러분의 pipeline이 요구사항을 만족하며 실행되고 있는지 확인하세요
"""

with DAG(???) as dag:
    pass




