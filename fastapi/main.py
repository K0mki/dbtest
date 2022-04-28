import subprocess
from unicodedata import name
from fastapi import Body, FastAPI, status, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from tortoise.contrib.fastapi import register_tortoise
from models import *
from typing import List, Optional, Set

app = FastAPI()


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


@app.post('/init',
          summary="Create database")
async def init():

    # subprocess.call("./dropdb.sh")  #TODO ??

    # TODO Clean up
    lookups = {'phone_types': {}}

    for pt_name in ('Mobile', 'Work', 'Home', 'Other'):
        pt = await PhoneType.filter(name=pt_name).get_or_none()
        if not pt:
            pt = PhoneType(name=pt_name)
            await pt.save()

        lookups['phone_types'][pt_name] = pt

    c1 = Contact(first_name='Stefan', last_name='Kotarac')
    await c1.save()
    p1 = PhoneNumber(phone_number='12345678',
                     phone_type=lookups['phone_types']['Mobile'], is_primary='True', contact_id=c1.id, note="Moj broj")
    p12 = PhoneNumber(phone_number='23456789',
                      phone_type=lookups['phone_types']['Work'], is_primary=False, contact_id=c1.id, note="Kucni broj")
    await p1.save()
    await p12.save()
    c2 = Contact(first_name='Marko', last_name='Markovic')
    await c2.save()
    p2 = PhoneNumber(phone_number='34567890',
                     phone_type=lookups['phone_types']['Work'], is_primary='True', contact_id=c2.id, note="Glavni broj")
    await p2.save()

    return {"Database": "created"}


@app.post('/contacts/types/add',
          tags=['phone types'],
          summary="Create phone type")
async def add_phone_type(phone: PhoneTypeIn_Pydantic):

    # types = PhoneType.fetch_related('name')                   # TODO Fix phone_types
    # if phone in types:
    #     return{'Error': 'Phone type already exists'}

    phone = await PhoneType.create(**phone.dict())

    return {"Created phone type": {phone}}


@app.post('/contacts/contact/add',
          tags=['contacts'],
          summary="Create contact")
async def add_contact(contact: ContactIn_Pydantic, phone: PhoneIn_Pydantic):
    """
    Create an contact with all the information:

    - **first_name**: contacts first name
    - **last_name**: contacts last name
    - **phone_number**: required
    - **phone_type**: type of phone connected to this number
    - **is_primary**: chose if this is contacts primary number
    - **note**: note , not required

    """
    # lookups = {'phone_types': {}}             # TODO Fix phone_types
    # pt = await PhoneType.filter(name=phone_type.name.capitalize).get_or_none()
    # if not pt:
    #     raise HTTPException(status_code=404, detail='Phone type not found')
    # lookups['phone_types'][phone_type.name] = pt

    contact = await Contact.create(**contact.dict(exclude_unset=True))
    phone = await PhoneNumber.create(**phone.dict(exclude_unset=True))
    name = contact.first_name
    return {"Created contact": {name}}


@app.post('/contacts/phone/add',
          tags=['phone number'],
          summary="Create phone number")
async def add_phone(phone: PhoneIn_Pydantic):

    # lookups = {'phone_types': {}}             # TODO Fix phone_types
    # pt = await PhoneType.filter(name=phone_type.name.capitalize).get_or_none()
    # if not pt:
    #     raise HTTPException(status_code=404, detail='Phone type not found')
    # lookups['phone_types'][phone_type.name] = pt

    phone = await PhoneNumber.create(**phone.dict(exclude_unset=True))
    return {"Created phone": {phone}}


@app.get("/contacts/all",
         summary="List all information")
async def all_info():
    contacts = await Contact_Pydantic.from_queryset(Contact.all())
    phones = await Phone_Pydantic.from_queryset(PhoneNumber.all())
    types = await PhoneType_Pydantic.from_queryset(PhoneType.all())
    return {'Phone types': types}, {'Contacts': contacts}, {'Phone numbers': phones}


@app.get("/contacts/type",
         tags=['phone types'],
         summary="List all phone types")
async def all_types():
    types = await PhoneType_Pydantic.from_queryset(PhoneType.all())
    return {'Phone types': types}


@app.get("/contacts/contact",
         tags=['contacts'],
         summary="List all contacts")
async def all_contacts():
    contact = await Contact_Pydantic.from_queryset(Contact.all())
    return {'Contacts': contact}


@app.get("/contacts/phone",
         tags=['phone number'],
         summary="List all phone numbers"
         )  # TODO Not listing contact ID and phone types
async def all_phones():
    phone = await Phone_Pydantic.from_queryset(PhoneNumber.all())
    return {'Phones': phone}


@app.put("/contacts/{contact_id}",
         response_model=Contact_Pydantic,
         summary="Edit contact"
         )
# TODO Fix relations
async def update_contact(contact_id: str, contact: ContactIn_Pydantic, phone: PhoneIn_Pydantic):
    c = await Contact.get(id=contact_id)
    p = await PhoneNumber.get(contact_id=contact_id)
    c_model = ContactIn_Pydantic(**c)
    p_model = PhoneIn_Pydantic(**p)
    update_c = contact.dict(exclude_unset=True)
    update_p = phone.dict(exclude_unset=True)
    updated_c = c_model.copy(update=update_c)
    updated_p = p_model.copy(update=update_p)
    await Contact.filter(id=contact_id).update(**{updated_c})
    await PhoneNumber.filter(contacts_id=contact_id).update(**{updated_p})
    return await Contact_Pydantic.from_tortoise_orm(contact)


# DELETE /settings/type/:id_type 
@app.delete('/contacts/type/delete/{type_id}', tags=['phone types'], summary="Delete phone type")
async def delete(type_id: str):
    await PhoneType.filter(id=type_id).delete()
    return{"Phone type deleted": {type_id}}


# DELETE /contats/:id_contat
@app.delete('/contacts/contact/delete/{contact_id}', tags=['contacts'], summary="Delete contact")
async def delete(contact_id: str):
    await Contact.filter(id=contact_id).delete()
    return{"Contact deleted": {contact_id}}


@app.delete('/contacts/phone/delete/{phone_id}', tags=['phone number'], summary="Delete phone number")
async def delete_phone(phone_id: str):
    await PhoneNumber.filter(id=phone_id).delete()
    return{"Phone deleted": {phone_id}}


register_tortoise(
    app,
    db_url='postgres://stefan:123@localhost:5432/adr',
    modules={'models': ['main']},
    generate_schemas=True
)
