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

    phone: fields.ReverseRelation['PhoneNumber']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} "+' '.join([f'\n   {("Primary " if pno.is_primary == True else "x  "):^9} {pno.phone_number} ({pno.phone_type.name:^6})   {pno.note:<10} ' for pno in self.phone])      # ? 


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