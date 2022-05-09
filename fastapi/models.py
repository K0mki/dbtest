from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt


class User(Model):
    class Meta:
        table = "user_info"

    id = fields.IntField(pk=True)
    username = fields.CharField(64, unique=True)
    password_hash = fields.CharField(128)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)


User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)


class PhoneType(Model):
    class Meta:
        table = 'lookup_phone_types'

    id = fields.UUIDField(pk=True)
    name = fields.CharField(16, unique=True)


PhoneType_Pydantic = pydantic_model_creator(PhoneType, name='PhoneType')
PhoneTypeIn_Pydantic = pydantic_model_creator(PhoneType, name='PhoneTypeIn', exclude_readonly=True)


class Contact(Model):
    class Meta:
        table = 'contacts'

    id = fields.UUIDField(pk=True)
    first_name = fields.TextField()
    last_name = fields.TextField()


Contact_Pydantic = pydantic_model_creator(Contact, name='Contact')
ContactIn_Pydantic = pydantic_model_creator(Contact, name='ContactIn', exclude_readonly=True)


class PhoneNumber(Model):
    class Meta:
        table = 'phone_numbers'

    id = fields.UUIDField(pk=True)
    phone_number = fields.TextField()
    is_primary = fields.BooleanField(null=True)
    note = fields.TextField(null=True)

    contact = fields.ForeignKeyField(
        "models.Contact", related_name="phone_numbers"
    )
    phone_type =  fields.ForeignKeyField(
        "models.PhoneType", related_name="phone_numbers",to_field = 'name'
    )
    


Phone_Pydantic = pydantic_model_creator(PhoneNumber, name='PhoneNumber')
PhoneIn_Pydantic = pydantic_model_creator(PhoneNumber, name='PhoneNumberIn', exclude_readonly=True)
