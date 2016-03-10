create database if not exists mlplatform default charset utf8 COLLATE utf8_general_ci;
use mlplatform;
alter table dataset(
	id int(4) not null primary key auto_increment
	,name varchar(20) not null
	,type int(1) not DEFAULT 0 --0 local 1 online
	,path varchar(255) --filepath local url online
	,filetype varchar(10)
	,head varchar(1023)
	,attr_delim varchar(3)
	,record_delim varchar(3)
	,location varchar(255)
	,search varchar(255)
)
alter table model(
	id int(4) not null primary key auto_increment
	,name varchar(20) not null
	,path varchar(255)
	,modeltype varchar(10)
)
