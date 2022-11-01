CREATE database dataset;
create user dataengineer with password 'dataengineer';

\c dataset;

create table covid(
    country varchar(100) not null,
    acc_confirmed int not null,
    death int not null,
    recovered int not null,
    active int not null,
    datadate timestamp not null
);
CREATE INDEX btree_covid_datadate on covid(datadate);
ALTER TABLE covid OWNER TO dataengineer;

create table air_quality(
    country varchar(100) not null,
    measurement real not null,
    datadate timestamp not null
);
ALTER TABLE air_quality OWNER TO dataengineer;

create table population(
    country varchar(100) not null,
    code varchar(10) not null,
    data_year int not null,
    num bigint not null
);
ALTER TABLE population OWNER TO dataengineer;

grant ALL PRIVILEGES on database dataset to dataengineer;
grant all PRIVILEGES on ALL TABLES IN SCHEMA public TO dataengineer;