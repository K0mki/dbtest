
# inicijalizacija

python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt



# resetovanje base

# potrebno je napraviti korisnika i bazu addressbook

# as admin user:
create user stefan with createdb login password '123';

# as stefan
psql -U stefan template1
psql -U stefan addressbook < ab.sql 

