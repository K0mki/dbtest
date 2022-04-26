import subprocess
from fastapi import FastAPI, status
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from models import *
from typing import Optional

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

    
# TODO Tests

# /contacts

#         POST            - creating
#         GET             - listing, filtering, searching

#         /contacts/{id_of_contact}

#         GET             - fetch single contact
#         PATCH           - change one property
#         PUT             - change whole contact
#         DELETE          - remove contact



@app.get("/") 
async def index():
    return {'Message': 'Go to http://127.0.0.1:8000/docs for the API doc'}


@app.post('/init')
async def init():

    # subprocess.call("./dropdb.sh")  #TODO ??

    #TODO Clean up
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

    return {"Database" : "created"} 


@app.post('/contacts/types/add')            # TODO Fix, multiple types, 
async def add_phone_type(phone: str):
    lookups =  {'phone_types':{}}
    pt = await PhoneType.filter(name=phone.capitalize()).get_or_none()
    if phone in pt: 
        return{'Error':'Phone type already exists'}
    lookups['phone_types'][phone]=pt    
    type = PhoneType(name = phone)    
    type.save()
    return {"Created phone type":{phone}}


@app.post('/contacts/contact/add')      # TODO Returns code 200 OK when wrong phone type is entered
async def add_contact(
    first_name:str, last_name:str, phone_number:str,phone_type:str, is_primary:bool, note:Optional[str] = None      #TODO phone_type Enum?
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

@app.post('/contacts/phone/add')        # TODO Returns code 200 OK when wrong phone type is entered
async def add_phone(
    contact_id:str,phone_number:str,phone_type:str, is_primary:bool, note:Optional[str] = None          #TODO phone_type Enum?
):
    lookups =  {'phone_types':{}}
    pt = await PhoneType.filter(name=phone_type.capitalize()).get_or_none()
    if not pt: 
        return{'Error':'Invalid phone type'}
    lookups['phone_types'][phone_type]=pt    

    phone = PhoneNumber( phone_number = phone_number , phone_type = lookups['phone_types'][phone_type.capitalize()] , is_primary = is_primary , contact_id = contact_id ,note = note)
    await phone.save()
    return {"Added phone to contact":{contact_id}}


@app.get("/contacts/all") 
async def all_info():
    contacts = await Contact_Pydantic.from_queryset(Contact.all())
    phones = await Phone_Pydantic.from_queryset(PhoneNumber.all())
    types = await PhoneType_Pydantic.from_queryset(PhoneType.all())
    return {'Phone types' :types} , {'Contacts':contacts} , {'Phone numbers':phones}


@app.get("/contacts/type") 
async def all_types():   
    types = await PhoneType_Pydantic.from_queryset(PhoneType.all())                                                                             
    return {'Phone types' : types}


@app.get("/contacts/contact") 
async def all_contacts():
    contact = await Contact_Pydantic.from_queryset(Contact.all())
    return {'Contacts' : contact}


@app.get("/contacts/phone")         #TODO Not listing contact ID and phone types
async def all_phones():  
    phone = await Phone_Pydantic.from_queryset(PhoneNumber.all())                                                                              
    return {'Phones' : phone}


@app.put("/contacts/{contact_id}",response_model=Contact_Pydantic)       #TODO Add other models to update, add PATCH
async def update_contact(contact_id: str , contact:ContactIn_Pydantic ):
    update_c = await Contact.get(id=contact_id)
    # update_p = await PhoneNumber.get(contact_id = update_c.id)
    # update_t = await PhoneType.get(id = update_p.phone_type_id)

    update_c.update(contact.dict(exclude_unset=True))
    # update_p.update(phone.dict(exclude_unset=True))
    # update_t.update(type.dict(exclude_unset=True))
    # contact.first_name = update_c['first_name']
    # contact.last_name = update_c['last_name']
    # await contact.save()
    # return await Contact_Pydantic.from_tortoise_orm(contact)


# @app.patch("/contacts/{contact_id}",response_model=Contact_Pydantic,status_code=status.HTTP_200_OK)
# async def update_contact_partial(contact_id: str , update:ContactIn_Pydantic):
#     contact = await Contact.get(id=contact_id)
#     update = update.dict(exclude_unset=True)
#     contact.first_name = update['first_name']
#     contact.last_name = update['last_name']
#     await contact.save()
#     return await Contact_Pydantic.from_tortoise_orm(contact)


@app.delete('/contacts/{type_id}')
async def delete(type_id: str):
    await PhoneType.filter(id=type_id).delete()
    return{"Phone type deleted": {type_id}}


@app.delete('/contacts/{contact_id}')
async def delete(contact_id: str):
    await Contact.filter(id=contact_id).delete()
    return{"Contact deleted": {contact_id}}


@app.delete('/contacts/{phone_id}')
async def delete_phone(phone_id: str):
    await PhoneNumber.filter(id=phone_id).delete()
    return{"Phone deleted": {phone_id}}


register_tortoise(
    app,
    db_url='postgres://stefan:123@localhost:5432/adr',
    modules={'models':['main']},
    generate_schemas=True
    ) 