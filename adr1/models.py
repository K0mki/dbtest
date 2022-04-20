from tortoise import fields
from tortoise.models import Model 
from tortoise.contrib.pydantic import pydantic_model_creator

class PhoneType(Model):
    class Meta: 
        table='lookup_phone_types'
    
    id = fields.UUIDField(pk=True)
    name = fields.CharField(8)
    
    def __str__(self):
        return f'{self.id} {self.name}'


class PhoneNumber(Model):
    class Meta:
        table='phone_numbers'

    id = fields.UUIDField(pk = True)
    phone_number = fields.TextField()
    is_primary = fields.BooleanField(null = True)                            
    note = fields.TextField(null=True)

     
    def __str__(self):
        return f"{self.id} {self.phone_number} {self.phone_type} {self.note}"


class Contact(Model):
    class Meta:
        table='contacts'

    id = fields.UUIDField(pk = True)
    first_name = fields.TextField()
    last_name = fields.TextField()

    phone: fields.ReverseRelation['PhoneNumber']

    
    def __str__(self):
        return f"{self.first_name} {self.last_name} "+' '.join([f'\n   {("Primary " if pno.is_primary == True else "x  "):^9} {pno.phone_number} ({pno.phone_type.name:^6})   {pno.note:<10} ' for pno in self.phone])      

PhoneType_Pydantic = pydantic_model_creator(PhoneType, name='PhoneType') 
PhoneTypeIn_Pydantic = pydantic_model_creator(PhoneType, name='PhoneTypeIn',exclude_readonly=True) 

Phone_Pydantic = pydantic_model_creator(PhoneNumber, name='PhoneNumber')
PhoneIn_Pydantic = pydantic_model_creator(PhoneNumber, name='PhoneNumberIn',exclude_readonly=True)

Contact_Pydantic = pydantic_model_creator(Contact, name='Contact')
ContactIn_Pydantic = pydantic_model_creator(Contact, name='ContactIn',exclude_readonly=True)

contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact",related_name="phone")
phone_type : fields.ForeignKeyRelation[PhoneType] = fields.ForeignKeyField("models.PhoneType")
