#!.venv/bin/python
from models import *  
from functions import *
from tortoise import run_async

# TODO  Make and fix functions
# TODO  Fix models
# TODO  Bash scripts ; drop/create database , insert test contacts ...
# TODO  Make tests

if __name__ == "__main__":
    run_async(create())
    add_contact('Stefan' , 'Kotarac' , '12345678' , 'mobile' , 'True' , 'Moj broj')
