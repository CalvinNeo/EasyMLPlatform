create database if not exists mlplatform default charset utf8 COLLATE utf8_general_ci;
use mlplatform;
create table dataset(id int(4) not null primary key auto_increment
	,name varchar(20) not null
	,path varchar(255)
	,filetype varchar(10)
	,head varchar(1023)
	,attr_delim varchar(3)
	,record_delim varchar(3)
)
