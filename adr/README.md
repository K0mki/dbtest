cd work/dbtest/adr
python3 -m venv .venv &&. .venv/bin/activate && pip install -r requirements.txt

sudo su
su postgres
psql
\c postgres
drop database adr;
create database adr;
\c adr

psql -U stefan template1 -c 'drop database adr;' -c 'create database adr;'

psql -U stefan adr | select * from lookup_phone_types; select * from contacts; select * from phone_numbers;


select * from search_list;