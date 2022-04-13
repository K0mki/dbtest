#!.venv/bin/python
from models import *  
from functions import *
from tortoise import run_async

#./adr.py  izbacuje sta radi program
#./adr.py  -h  izbacuje sve funkcije programa i kako se koriste
#./adr.py  --setup  droppuje i pravi bazu i dodaje nekoliko test korisnika
#./adr.py  -a ... -l  .....

if __name__ == "__main__":
    run_async(arg())
    # run_async(setup())
    # run_async(add_contact('Test', 'Test' , '1234', 'mobile' , "da" , 'test br'))
    # run_async(add_number(c2.id , '23456', work , "dsadsadsa" , 'test br 2'))
    # run_async(remove_contact('first_name', 'Stefan'))
    # run_async(update_contact('341abf6c-0c66-4026-9eef-9901f10282d6', 'note', 'Moj glavni broj'))
    # run_async(search_contacts('first_name', 'Stefan'))
    # run_async(detailed_contact("341abf6c-0c66-4026-9eef-9901f10282d6")) #??
    # run_async(all_contacts("first_name", "desc"))
    