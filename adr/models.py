from tortoise import fields 
from tortoise.models import Model 

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

    phone_numbers: fields.ReverseRelation['PhoneNumber']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} "+' '.join([f'{pno.phone_number} ({pno.phone_type.name})' for pno in self.phone_numbers])          

class PhoneNumber(Model):
    class Meta:
        table='phone_numbers'

    id = fields.UUIDField(pk = True)
    phone_number = fields.TextField()
    is_primary = fields.BooleanField(null = True)                            
    note = fields.TextField(null=True)

    contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact",related_name="phone_numbers")
    phone_type : fields.ForeignKeyRelation[PhoneType] = fields.ForeignKeyField("models.PhoneType")

# class SearchList(Model):
#     class Meta:
#         table='search_list'

#     id = fields.IntField(pk=True)
#     contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact")
#     phone_numbers : fields.ForeignKeyField[PhoneNumber] = fields.ForeignKeyField('model.PhoneNumber')
#     phone_type : fields.ForeignKeyField[PhoneType] = fields.ForeignKeyField('model.PhoneType')
#     search: fields.TextField(null=True)  