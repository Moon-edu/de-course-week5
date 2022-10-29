CREATE database covid;
create user dataengineer with password 'dataengineer';
grant ALL on database covid to dataengineer;

create table covid(
    country varchar(100) not null,
    confirmed int not null,
    death int not null,
    datadate varchar(12) not null
);

create table air_quality(
    country varchar(100) not null,
    measurement double not null,
    datadate varchar(12) not null
);

create table population(
    country varchar(100) not null,
    code varchar(10) not null,
    data_year int not null,
    num bigint not null
);
