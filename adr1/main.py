import subprocess
from fastapi import FastAPI, status
from pydantic import BaseModel
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


@app.post('/init')
async def init():
    # subprocess.call("./setup.sh")

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

@app.post('/types')
async def add_phone_type(phone: PhoneTypeIn_Pydantic):
    lookups =  {'phone_types':{}}
    
    for pt_name in ('Mobile','Work','Home','Other'):
        pt = await PhoneType.filter(name=pt_name).get_or_none()
        if not pt:
            pt = PhoneType(name=pt_name)
            await pt.save()    
        
        lookups['phone_types'][pt_name]=pt
    name = phone.name
    await PhoneType.create(**phone.dict())
    return {"Created phone type":{name}}


@app.post('/contacts')
async def add_contact(
    first_name:str, last_name:str, phone_number:str,phone_type:str, is_primary:bool, note:Optional[str] = None 
):
    lookups =  {'phone_types':{}}
    pt = await PhoneType.filter(name=phone_type.capitalize()).get_or_none()
    if not pt: 
        return{'Error':'Invalid phone type'}
    lookups['phone_types'][phone_type]=pt    
    
    contact =  Contact( first_name = first_name , last_name = last_name)
    await contact.save()
    phone =  PhoneNumber( phone_number = phone_number , phone_type = lookups['phone_types'][phone_type] , is_primary = is_primary , contact_id = contact.id ,note = note)
    await phone.save()
    return {"Created contact":{first_name}}


# @app.post('/contacts')
# async def add_contact2(contact: ContactIn_Pydantic, phone: PhoneIn_Pydantic ):

#     contact = await Contact.create(**contact.dict(exclude_unset=True))
#     phone = await PhoneNumber.create(**phone.dict(exclude_unset=True))
#     name = contact.first_name
#     return {"Created contact":{name}}


@app.get("/info") 
async def all_info():
    contacts = await Contact_Pydantic.from_queryset(Contact.all())
    phones = await Phone_Pydantic.from_queryset(PhoneNumber.all())
    types = await PhoneType_Pydantic.from_queryset(PhoneType.all())
    return {'Phone types' :types} , {'Contacts':contacts} , {'Phone numbers':phones}


@app.get("/types") 
async def all_types():                                                                                
    return await PhoneType_Pydantic.from_queryset(PhoneType.all())


@app.get("/contacts") 
async def all_contacts():                                                                                
    return await Contact_Pydantic.from_queryset(Contact.all())


@app.get("/phones") 
async def all_phones():                                                                                
    return await Phone_Pydantic.from_queryset(PhoneNumber.all())



@app.put("/contacts/{contact_id}",response_model=Contact_Pydantic,status_code=status.HTTP_200_OK)
async def update_contact(contact_id: str , update_c:ContactIn_Pydantic, update_p:PhoneIn_Pydantic, update_t:PhoneTypeIn_Pydantic):
    contact = await Contact.get(id=contact_id)
    update_c = update_c.dict(exclude_unset=True)
    contact.first_name = update_c['first_name']
    contact.last_name = update_c['last_name']
    await contact.save()
    return await Contact_Pydantic.from_tortoise_orm(contact)


# @app.patch("/contacts/{contact_id}",response_model=Contact_Pydantic,status_code=status.HTTP_200_OK)
# async def update_contact_partial(contact_id: str , update:ContactIn_Pydantic):
#     contact = await Contact.get(id=contact_id)
#     update = update.dict(exclude_unset=True)
#     contact.first_name = update['first_name']
#     contact.last_name = update['last_name']
#     await contact.save()
#     return await Contact_Pydantic.from_tortoise_orm(contact)


@app.delete('/types/{type_id}')
async def delete(type_id: str):
    await PhoneType.filter(id=type_id).delete()
    return{"Contact deleted": {type_id}}

@app.delete('/contacts/{contact_id}')
async def delete(contact_id: str):
    await Contact.filter(id=contact_id).delete()
    return{"Contact deleted": {contact_id}}

@app.delete('/phones/{phone_id}')
async def delete_phone(phone_id: str):
    await PhoneType.filter(id=phone_id).delete()
    return{"Phone type deleted": {phone_id}}


register_tortoise(
    app,
    db_url='postgres://stefan:123@localhost:5432/adr',
    modules={'models':['main']},
    generate_schemas=True
    ) 