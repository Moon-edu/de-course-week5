create table stock(
	code varchar(10) not null,
	name varchar(10) not null,
	price int not null,
	price_date varchar(15) not null,
	category varchar(30) not null
);


insert into stock values('A0000', '오성전자', 10000, '2022-01-01', '전자기기');
insert into stock values('A0000', '오성전자', 10000, '2022-01-02', '전자기기');
insert into stock values('A0000', '오성전자', 10000, '2022-01-03', '전자기기');
insert into stock values('A0000', '오성전자', 10000, '2022-01-04', '전자기기');
insert into stock values('A0000', '오성전자', 10000, '2022-01-05', '전자기기');