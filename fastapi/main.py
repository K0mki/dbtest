from fastapi import FastAPI, status
from tortoise.contrib.fastapi import register_tortoise
from models import *
from typing import Optional

app = FastAPI()

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


@app.post('/init')
async def init():

    # subprocess.call("./dropdb.sh")  #TODO ??

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

    return ("Database created") 

@app.post('/contacts/types')
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


# TODO Returns code 200 OK when wron phone type is entered
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

# TODO Returns code 200 OK when wron phone type is entered
@app.post('/contacts/phones')
async def add_phone(
    contact_id:str,phone_number:str,phone_type:str, is_primary:bool, note:Optional[str] = None 
):
    lookups =  {'phone_types':{}}
    pt = await PhoneType.filter(name=phone_type.capitalize()).get_or_none()
    if not pt: 
        return{'Error':'Invalid phone type'}
    lookups['phone_types'][phone_type]=pt    

    phone = PhoneNumber( phone_number = phone_number , phone_type = lookups['phone_types'][phone_type.capitalize()] , is_primary = is_primary , contact_id = contact_id ,note = note)
    await phone.save()
    return {"Added phone to contact":{contact_id}}

# TODO Needs formating
@app.get("/contacts/info") 
async def all_info():
    contacts = await Contact_Pydantic.from_queryset(Contact.all())
    phones = await Phone_Pydantic.from_queryset(PhoneNumber.all())
    types = await PhoneType_Pydantic.from_queryset(PhoneType.all())
    return {'Phone types' :types} , {'Contacts':contacts} , {'Phone numbers':phones}


@app.get("/contacts//types") 
async def all_types():                                                                                
    return await PhoneType_Pydantic.from_queryset(PhoneType.all())


@app.get("/contacts/all") 
async def all_contacts():                                                                                
    return await Contact_Pydantic.from_queryset(Contact.all())


@app.get("/contacts/phones") 
async def all_phones():                                                                                
    return await Phone_Pydantic.from_queryset(PhoneNumber.all())


#TODO Add other models to update, add PATCH
@app.put("/contacts/update/{contact_id}",response_model=Contact_Pydantic,status_code=status.HTTP_200_OK)
async def update_contact(contact_id: str , update_c:ContactIn_Pydantic):
    contact = await Contact.get(id=contact_id)
    update_c = update_c.dict(exclude_unset=True)
    # update_p = update_p.dict(exclude_unset=True)
    # update_t = update_t.dict(exclude_unset=True)
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


@app.delete('/contacts/types/delete/{type_id}')
async def delete(type_id: str):
    await PhoneType.filter(id=type_id).delete()
    return{"Phone type deleted": {type_id}}

@app.delete('/contacts/delete/{contact_id}')
async def delete(contact_id: str):
    await Contact.filter(id=contact_id).delete()
    return{"Contact deleted": {contact_id}}

@app.delete('/contacts/phones/delete/{phone_id}')
async def delete_phone(phone_id: str):
    await PhoneNumber.filter(id=phone_id).delete()
    return{"Phone deleted": {phone_id}}


register_tortoise(
    app,
    db_url='postgres://stefan:123@localhost:5432/adr',
    modules={'models':['main']},
    generate_schemas=True
    ) 