from fastapi import FastAPI, Path, Query , HTTPException, status
from typing import Optional
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from tortoise import fields 
from tortoise.models import Model 
from tortoise.contrib.pydantic import pydantic_model_creator

app = FastAPI()

db = []

class PhoneType(Model):
    class Meta: 
        table='lookup_phone_types'
    
    id = fields.UUIDField(pk=True)
    name = fields.CharField(8)
    
    def __str__(self):
        return f'{self.id} {self.name}'


class Contact(Model):
    class Meta:
        table='contacts'

    id = fields.UUIDField(pk = True)
    first_name = fields.TextField()
    last_name = fields.TextField()

    phone: fields.ReverseRelation['PhoneNumber']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} "+' '.join([f'\n   {("Primary " if pno.is_primary == True else "x  "):^9} {pno.phone_number} ({pno.phone_type.name:^6})   {pno.note:<10} ' for pno in self.phone])      # ? 

Contact_Pydantic = pydantic_model_creator(Contact, name='Contact')
ContactIn_Pydantic = pydantic_model_creator(Contact, name='ContactIn',exclude_readonly=True)

class PhoneNumber(Model):
    class Meta:
        table='phone_numbers'

    id = fields.UUIDField(pk = True)
    phone_number = fields.TextField()
    is_primary = fields.BooleanField(null = True)                            
    note = fields.TextField(null=True)

    contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact",related_name="phone")
    phone_type : fields.ForeignKeyRelation[PhoneType] = fields.ForeignKeyField("models.PhoneType")
    
    def __str__(self):
        return f"{self.id} {self.phone_number} {self.phone_type} {self.note}"

Phone_Pydantic = pydantic_model_creator(PhoneNumber, name='PhoneNumber')
PhoneIn_Pydantic = pydantic_model_creator(PhoneNumber, name='PhoneNumberIn',exclude_readonly=True)


@app.get("/")
async def index():
    return ('Hello')

# @app.post('/create-contact')
# async def create_contact(contact: ContactIn_Pydantic,phone: PhoneIn_Pydantic):
#     contact_obj = await Contact.create(**contact.dict(exclude_unset=True))
#     phone_obj = await PhoneNumber.create(**phone.dict(exclude_unset=True))
#     return await Contact_Pydantic.from_tortoise_orm(contact_obj)


# @app.get("/contacts") 
# async def all_contacts():                                                                                
#     contacts = await Contact.all().prefetch_related('phone','phone__phone_type')
#     for contact in contacts:
#         return contact
# return await City_Pydantic.from_queryset(City.all())
        

# @app.get("/get-contact/{contact_id}")
# async def detailed_contact(contact_id: int):                                                                           
#     '''
#         Show info for provided ID's contact
#     '''
#     contacts = await Contact.filter(id = contact_id).prefetch_related('phone','phone__phone_type')
#     for contact in contacts:
#         return contact
#     # return await City_Pydantic.from_queryset_single(City.get(id=city_id))


# @app.delete('/contacts/{contact_id}')
# async def delete_(contact_id: int):
#     await Contact.filter(id=contact_id).delete()
#     return {}


# @app.delete("/delete-contact")
# async def delete_contact(contact_id:int ):
#     await Contact.filter(id=contact_id).delete()
#     return{"Succes": "Item deleted"}


register_tortoise(
    app,
    db_url='postgres://stefan:123@localhost:5432/adr',
    modules={'models':['main']},
    generate_schemas=True
    )