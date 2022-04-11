#!/bin/bash

cd work/dbtest/addressbook

sudo -iu postgres
psql

drop database adr;
create database adr;
\q

drop database adr;
create database adr;
\c adr

select * from lookup_phone_types;
select * from contacts;
select * from phone_numbers;