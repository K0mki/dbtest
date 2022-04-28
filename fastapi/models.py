from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class PhoneType(Model):
    class Meta:
        table = 'lookup_phone_types'

    id = fields.UUIDField(pk=True)
    name = fields.CharField(16)


class PhoneNumber(Model):
    class Meta:
        table = 'phone_numbers'

    id = fields.UUIDField(pk=True)
    phone_number = fields.TextField()
    is_primary = fields.BooleanField(null=True)
    note = fields.TextField(null=True)


class Contact(Model):
    class Meta:
        table = 'contacts'

    id = fields.UUIDField(pk=True)
    first_name = fields.TextField()
    last_name = fields.TextField()

    phone: fields.ReverseRelation['PhoneNumber']


contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField(
    "models.Contact")
phone_type: fields.ForeignKeyRelation[PhoneType] = fields.ForeignKeyField(
    "models.PhoneType")


PhoneType_Pydantic = pydantic_model_creator(PhoneType, name='PhoneType')
PhoneTypeIn_Pydantic = pydantic_model_creator(
    PhoneType, name='PhoneTypeIn', exclude_readonly=True)

Phone_Pydantic = pydantic_model_creator(PhoneNumber, name='PhoneNumber')
PhoneIn_Pydantic = pydantic_model_creator(
    PhoneNumber, name='PhoneNumberIn', exclude_readonly=True)

Contact_Pydantic = pydantic_model_creator(Contact, name='Contact')
ContactIn_Pydantic = pydantic_model_creator(
    Contact, name='ContactIn', exclude_readonly=True)
