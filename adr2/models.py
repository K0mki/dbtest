from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.TextField()
    age = fields.IntField()

    class Meta:
        table= "users"
    
    def __str__(self):
        return f"{self.id}, {self.username}, {self.age}"
