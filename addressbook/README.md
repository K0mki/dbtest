# inicijalizacija

cd work/dbtest/addressbook
python3 -m venv .venv &&. .venv/bin/activate && pip install -r requirements.txt

# resetovanje base

# potrebno je napraviti korisnika i bazu 

<!-- sudo -iu postgres
psql
createdb -h localhost -p 5432 -U stefan adr
psql -h localhost -U stefan -d adr -f /home/stefan/work/dbtest/addressbook/ab.py -->

# as admin user:

create user stefan with createdb login password '123';

# as stefan:

psql -U stefan template1
psql -U stefan addressbook < ab.sql 

