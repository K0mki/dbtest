import jwt
from unicodedata import name
from xml.dom.minidom import TypeInfo
from fastapi import Body, Depends, FastAPI, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, HttpUrl
from tortoise.contrib.fastapi import register_tortoise
from passlib.hash import bcrypt
from models import *
from typing import List, Optional, Set

app = FastAPI()

SECRET_KEY = 'secret'


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


@app.get("/")
async def index():
    return {'Message': 'Go to http://127.0.0.1:8000/docs for the API doc'}


@app.post('/init',
          summary="Create database")
async def init():

    lookups = {'phone_types': {}}

    for pt_name in ('Mobile', 'Work', 'Home', 'Other'):
        pt = await PhoneType.filter(name=pt_name).get_or_none()
        if not pt:
            pt = PhoneType(name=pt_name)
            await pt.save()

        lookups['phone_types'][pt_name] = pt

    u1 = User(username='stefan', password_hash=bcrypt.hash('password'))
    await u1.save()
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

#-----------------------USER---------------------------#
# TODO ID isn't UUDI / TypeError: Object of type UUID is not JSON serializable


@app.post('/token',
          tags=['users'],
          summary="User token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid username or password')

    user_obj = await User_Pydantic.from_tortoise_orm(user)

    token = jwt.encode(user_obj.dict(), SECRET_KEY)

    return {'access_token': token, 'token_type': 'bearer'}


@app.post('/api/users',  # Create User
          tags=['users'],
          summary="Create user",
          response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username,
                    password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


@app.get('/api/users',  # List all users
         tags=['users'],
         summary="Get all users")
async def get_all_users():
    users = await User_Pydantic.from_queryset(User.all())
    return {"Users": users}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid username or password')

    return await User_Pydantic.from_tortoise_orm(user)


@app.get('/users/me',
         tags=['users'],
         summary="Current user",
         response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user
#-------------------------------------------------------#

@app.get("/api/test",
         summary="List all information")
async def test(contact_id : str):
    c = await Contact.get(id=contact_id)
    p = await PhoneNumber.filter(contact_id=c.id)
 

    # ph = await PhoneNumber.all()
    # phones = await Phone_Pydantic.from_queryset(PhoneNumber.all())

    return {'Contact':c} , {'Phone numbers':p}

@app.get("/api/contacts/all",
         summary="List all information")
async def all_info():
    users = await User_Pydantic.from_queryset(User.all())
    contacts = await Contact_Pydantic.from_queryset(Contact.all())
    phones = await Phone_Pydantic.from_queryset(PhoneNumber.all())
    types = await PhoneType_Pydantic.from_queryset(PhoneType.all())
    return {'Users': users}, {'Phone types': types}, {'Contacts': contacts}, {'Phone numbers': phones}


@app.post('/api/contacts/type/add',
          tags=['phone types'],
          summary="Create phone type",
          )
async def create_phone_type(phone: PhoneTypeIn_Pydantic):
    try:
        type_obj = PhoneType(name=phone.name.capitalize())
        await type_obj.save()
        return await PhoneType_Pydantic.from_tortoise_orm(type_obj)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Phone type already exists')


@app.get("/api/contacts/types",
         tags=['phone types'],
         summary="List all phone types")
async def read_types():
    types = await PhoneType_Pydantic.from_queryset(PhoneType.all())
    return {'Phone types': types}


@app.put("/api/contacts/type/edit/{type_id}",
         tags=['phone types'],
         response_model=PhoneType_Pydantic,
         summary="Edit phone type"
         )
async def update_type(type_id: str, type: PhoneTypeIn_Pydantic):
    try:
        t = await PhoneType.get(id=type_id)
        t.name = type.name.capitalize()
        await t.save()
        return t
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Phone type already exists")


@app.delete('/api/contacts/type/delete/{type_id}',                  
            tags=['phone types'],
            summary="Delete phone type")
async def delete_type(type_id: str):
    try:
        await PhoneType.filter(id=type_id).delete()
        return {'Phone type deleted': {type_id}}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Phone type doesn't exists")


@app.post('/api/contacts/contact/add',
          tags=['contacts'],
          summary="Create contact")
async def create_contact(contact: ContactIn_Pydantic, phone: PhoneIn_Pydantic, type: PhoneTypeIn_Pydantic):
    """
    Create an contact with all the information:

    - **first_name**: contacts first name
    - **last_name**: contacts last name
    - **phone_number**: required
    - **phone_type**: type of phone connected to this number
    - **is_primary**: chose if this is contacts primary number
    - **note**: note , not required

    """

    try:
        contact = Contact(first_name=contact.first_name.capitalize(),
                          last_name=contact.last_name.capitalize())
        await contact.save()
        type = await PhoneType.get(name=type.name.capitalize())
        phone = PhoneNumber(phone_number=phone.phone_number, is_primary=phone.is_primary,
                            note=phone.note, contact=contact, phone_type=type)
        await phone.save()
        return {"Created contact": {contact}}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Phone type doesn't exists")

@app.get("/api/contacts/contacts/{phone_id}",                     
           tags=['contacts'],
           summary="Search contacts"
           )
async def search_contact(contact_id: str):

    c = await Contact.get(id=contact_id)
    p = await PhoneNumber.filter(contact_id=c.id)
 
    return {'Contact':c} , {'Phone numbers':p}

@app.get("/api/contacts/contacts",
         tags=['contacts'],
         summary="List all contacts")
async def read_contacts():
    contact = await Contact_Pydantic.from_queryset(Contact.all())
    return {'Contacts': contact}


@app.put("/api/contacts/contact/edit/{contact_id}",
         tags=['contacts'],
         response_model=Contact_Pydantic,
         summary="Edit contact"
         )
async def update_contact(contact_id: str, contact: ContactIn_Pydantic):
    c = await Contact.get(id=contact_id)
    c.first_name = contact.first_name.capitalize()
    c.last_name = contact.last_name.capitalize()
    await c.save()
    return c


@app.delete('/api/contacts/contact/delete/{contact_id}',
            tags=['contacts'],
            summary="Delete contact")
async def delete_contact(contact_id: str):
    try:
        await Contact.filter(id=contact_id).delete()
        return{"Contact deleted": {contact_id}}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,      # TODO Doesn't throw error sometimes
                            detail="Contact doesn't exist")      


@app.post('/api/contacts/phone/add',
          tags=['phone number'],
          summary="Create phone number")
async def create_phone(contact_id: str, phone: PhoneIn_Pydantic, type: PhoneTypeIn_Pydantic):

    try:
        contact = await Contact.get(id=contact_id)
        type = await PhoneType.get(name=type.name)
        phone = PhoneNumber(phone_number=phone.phone_number, is_primary=phone.is_primary,
                            note=phone.note, contact=contact, phone_type=type)
        await phone.save()
        return {"Added phone ": {phone.phone_number}}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Phone type doesn't exists")


@app.get("/api/contacts/phones",                        
         tags=['phone number'],
         summary="List all phone numbers"
         )
async def read_phones():
    phone = await PhoneNumber.all()
    return {'Phones': phone}


@app.put("/api/contacts/phone/edit/{phone_id}",                   # TODO Add phone_type for editing
           tags=['phone number'],
           summary="Edit phone number"
           )
async def update_phone(phone_id: str, phone: PhoneIn_Pydantic):
    p = await PhoneNumber.get(id=phone_id)
    p.phone_number = phone.phone_number
    p.is_primary = phone.is_primary
    p.note = phone.note
    await p.save()
    return p


@app.delete('/api/contacts/phone/delete/{phone_id}',
            tags=['phone number'],
            summary="Delete phone number")
async def delete_phone(phone_id: str):
    await PhoneNumber.filter(id=phone_id).delete()
    return{"Phone deleted": {phone_id}}


register_tortoise(
    app,
    db_url='postgres://stefan:123@localhost:5432/adr',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)
