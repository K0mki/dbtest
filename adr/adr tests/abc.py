#!.venv/bin/python
from tortoise import Tortoise, run_async, fields 
from tortoise.models import Model 
import uuid
def add_c(first_name, last_name):     #-c

    # await add_c(first_name="Boban", last_name="Rajovic")
    a = first_name 
    b = last_name = last_name 

    return print(a , b )
if __name__ == "__main__":
    add_c('Stefan' 'Kotarac')