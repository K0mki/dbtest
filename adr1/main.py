import subprocess
from fastapi import FastAPI, status
from tortoise.contrib.fastapi import register_tortoise
from models import *
from typing import Optional
from tortoise import Tortoise

app = FastAPI()

db = []

# TODO Implement other models into functions
# TODO Search by anything function
# TODO Tests

# /contacts

#         POST            - creating
#         GET             - listing, filtering, searchin

#         /contacts/{id_of_contact}

#         GET             - fetch single contact
#         PATCH           - change one property
#         PUT             - change whole contact
#         DELETE          - remove contact


@app.get("/")
async def index():
    return {'Message': 'Go to http://127.0.0.1:8000/docs for the API doc'}


# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Optional[str] = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}


@app.post('/setup')
async def setup():
    subprocess.call("./setup.sh")

    await Tortoise.init(db_url="postgres://stefan:123@localhost:5432/adr" , modules={"models": ["models"]}) 
    await Tortoise.generate_schemas()


    lookups =  {'phone_types':{}}
    
    for pt_name in ('Mobile','Work','Home','Other'):
        pt = await PhoneType.filter(name=pt_name).get_or_none()
        if not pt:
            pt = PhoneType(name=pt_name)
            await pt.save()    
        
        lookups['phone_types'][pt_name]=pt


    c1 = Contact(first_name ='Stefan', last_name = 'Kotarac')
    await c1.save()
    p1 = PhoneNumber( phone_number = '12345678', phone_type = lookups['phone_types']['Mobile'] , is_primary = 'True', contact_id = c1.id, note = "Moj broj" )
    p12 = PhoneNumber( phone_number = '23456789', phone_type = lookups['phone_types']['Work'] , is_primary = False, contact_id = c1.id, note = "Kucni broj" )
    await p1.save()
    await p12.save()
    c2 = Contact(first_name ='Marko', last_name = 'Markovic')
    await c2.save()
    p2 = PhoneNumber( phone_number = '34567890', phone_type = lookups['phone_types']['Work'] , is_primary = 'True', contact_id = c2.id, note = "Glavni broj" )
    await p2.save()

    return print ("Database created") 

@app.post('/phones')
async def create_phone(phone: PhoneTypeIn_Pydantic):
    name = phone.name
    await PhoneType.create(**phone.dict())
    return {"Created phone type":{name}}


@app.post('/contacts')
async def create_contact(
    first_name:str, last_name:str, contact_note:Optional[str],
    phone_number:str,phone_type:str, is_primary:bool, note:Optional[str]
    # contact: ContactIn_Pydantic, phone: PhoneIn_Pydantic 
):
    contact =  Contact( first_name = first_name , last_name = last_name, contact_note = contact_note)
    await contact.save()
    phone =  PhoneNumber( phone_number = phone_number , phone_type = phone_type, is_primary = is_primary , contact_id = contact.id ,note = note)
    await phone.save()
    # await Contact.create(**contact.dict(exclude_unset=True))
    # await PhoneNumber.create(**phone.dict(exclude_unset=True))
    return {"Created contact":{first_name}}


@app.get("/phones") 
async def all_phones():                                                                                
    await PhoneType_Pydantic.from_queryset(PhoneType.all())


@app.get("/contacts") 
async def all_contacts():                                                                                
    await Contact_Pydantic.from_queryset(Contact.all())
    await Phone_Pydantic.from_queryset(PhoneNumber.all())
    await PhoneType_Pydantic.from_queryset(PhoneType.all())
    return    

@app.get("/contacts/{info}")
async def get_contact(info: str):                                                                           
    return await Contact_Pydantic.from_queryset_single(Contact.get(id=info))


@app.put("/contacts/{contact_id}",response_model=Contact_Pydantic,status_code=status.HTTP_200_OK)
async def update_contact(contact_id: str , update:ContactIn_Pydantic):
    contact = await Contact.get(id=contact_id)
    update = update.dict(exclude_unset=True)
    contact.first_name = update['first_name']
    contact.last_name = update['last_name']
    await contact.save()
    return await Contact_Pydantic.from_tortoise_orm(contact)


@app.patch("/contacts/{contact_id}",response_model=Contact_Pydantic,status_code=status.HTTP_200_OK)
async def update_contact_partial(contact_id: str , update:ContactIn_Pydantic):
    contact = await Contact.get(id=contact_id)
    update = update.dict(exclude_unset=True)
    contact.first_name = update['first_name']
    contact.last_name = update['last_name']
    await contact.save()
    return await Contact_Pydantic.from_tortoise_orm(contact)


@app.delete('/contacts/{contact_id}')
async def delete_(contact_id: str):
    await Contact.filter(id=contact_id).delete()
    return{"Succes": "Item deleted"}


register_tortoise(
    app,
    db_url='postgres://stefan:123@localhost:5432/adr',
    modules={'models':['main']},
    generate_schemas=True
    ) 