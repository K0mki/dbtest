# inicijalizacija

cd work/dbtest/addressbook
python3 -m venv .venv &&. .venv/bin/activate && pip install -r requirements.txt

# resetovanje base

# potrebno je napraviti korisnika i bazu 

# sudo -iu postgres

# as admin user:
sudo su
su postgres
psql

create user stefan with createdb login password '123';
^D
exit
exit

# as stefan:
cd work/dbtest/addressbook

psql -U stefan template1 -c 'drop database addressbook' -c 'create database addressbook'

psql -U stefan addressbook < ab.sql 
