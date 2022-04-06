#!.venv/bin/python
import json
import argparse
from dataclasses import field
from enum import unique
import sys
import os
import uuid
from tortoise import Tortoise, run_async, fields 
from tortoise.models import Model 

class PhoneType(Model):
    class Meta:
        table='lookup_phone_types'
    
    id = fields.UUIDField(pk=True)
    name = fields.CharField(8)

class Contact(Model):
    class Meta:
        table='contacts'

    id = fields.UUIDField(pk = True)
    first_name = fields.TextField()
    last_name = fields.TextField()

    phone_numbers: fields.ReverseRelation['PhoneNumber']

    def __str__(self):
        return f"{self.first_name} {self.last_name} "+' '.join([f'{pno.phone_number} ({pno.phone_type.name})' for pno in self.phone_numbers])      # ? 

class PhoneNumber(Model):
    class Meta:
        table='phone_numbers'

    id = fields.UUIDField(pk = True)
    phone_number = fields.TextField()
    is_primary = fields.BooleanField(null = True, unique = True)                            
    note = fields.TextField(null=True)

    contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact",related_name="phone_numbers")

    phone_type : fields.ForeignKeyRelation[PhoneType] = fields.ForeignKeyField("models.PhoneType")

async def run():
    try:
        os.unlink('adr.sql')     # ?
    except:
        pass
        
    await Tortoise.init(db_url="postgres://stefan:123@localhost:5432/adr" ,modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    lookups = {'phone_types':{}}
    
    for pt_name in ('Mobile','Work','Home','Other'):
        pt = await PhoneType.filter(name=pt_name).get_or_none()
        if not pt:
            pt = PhoneType(name=pt_name)
            await pt.save()    
        
        lookups['phone_types'][pt_name]=pt

    # def j_serialize(s):
    #     if type(s)==PhoneType:
    #         return s.name
    #     return str(s)
        
    # print(json.dumps(lookups,indent=4,default=j_serialize))
    
    for x in [
        {"first_name":"Stefan","last_name":"Kotarac","phone_numbers": [{"type":"Mobile", "number":"123"}, {"type": "Home", "number": "345"}]},
        {"first_name":"Igor","last_name":"Jeremic","phone_numbers": [{"type":"Mobile", "number":"0695967576"}]},
        {"first_name":"Aleksandar","last_name":"Stojkovic","phone_numbers": [{"type":"Mobile", "number":"061234567"}]}
    ]:
        contact = Contact(first_name=x['first_name'], last_name=x['last_name'])
        await contact.save()
        await contact.fetch_related('phone_numbers')
        for pn in x['phone_numbers']:
            dbpn = PhoneNumber(contact=contact, phone_number=pn['number'], phone_type=lookups['phone_types'][pn['type']])
            await dbpn.save()
            
#            await contact.phone_numbers.add( PhoneNumber(contact=contact, phone_number=pn['number'], phone_type=lookups['phone_types'][pn['type']]))
            
        print(x)

async def run2():
    await Tortoise.init(db_url="sqlite://adr.sql",modules={"models": ["__main__"]})  #postgres://stefan:123@localhost:5432/adr.sql

    contacts = await Contact.all().prefetch_related('phone_numbers','phone_numbers__phone_type')
    for contact in contacts:
        print(contact)

async def run3_get_stefan():
    await Tortoise.init(db_url="sqlite://adr.sql",modules={"models": ["__main__"]})  #postgres://stefan:123@localhost:5432/adr.sql

    contacts = await Contact.filter(first_name='Stefan').prefetch_related('phone_numbers','phone_numbers__phone_type')
    for contact in contacts:
        print(contact)
    
async def run4_update_stefan():
    await Tortoise.init(db_url="sqlite://adr.sql",modules={"models": ["__main__"]})  #postgres://stefan:123@localhost:5432/adr.sql

    stefan = await Contact.filter(first_name='Stefan').prefetch_related('phone_numbers','phone_numbers__phone_type').get_or_none()
    if stefan:
        stefan.last_name="K"
        await stefan.save()
        
        
if __name__ == "__main__":

    run_async(run())
#    run_async(run4_update_stefan())
#    run_async(run3_get_stefan())


