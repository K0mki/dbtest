#!.venv/bin/python
from models import *  
from functions import *
from tortoise import run_async

#*args **kwargs
#logovanje 
#fastAPI
#testove popraviti

#./adr.py  izbacuje sta radi program
#./adr.py  -h  izbacuje sve funkcije programa i kako se koriste
#./adr.py  --setup  droppuje i pravi bazu i dodaje nekoliko test korisnika
#./adr.py  -a ... -l  .....

if __name__ == "__main__":
    run_async(arg())