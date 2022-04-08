#!/bin/bash

cd work/dbtest/addressbook

sudo -iu postgres
psql

drop database adr;
create database adr;
\q


psql -U stefan template1 -c 'drop database adr' -c 'create database adr'


drop database adr;
create database adr;
\c adr

select * from lookup_phone_types;
select * from contacts;
select * from phone_numbers;