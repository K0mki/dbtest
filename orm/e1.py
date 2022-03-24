from tornado.httpclient import AsyncHTTPClient

from tortoise import Tortoise, fields, run_async
from tortoise.models import Model


class Contact(Model):
    class Meta:
        table = "contacts"
        
    id = fields.UUIDField(pk=True)

    first_name = fields.CharField(max_length=32, index=True)
    last_name = fields.CharField(max_length=32, index=True, null=True)
    
    phone_number = fields.CharField(max_length=32, index=True, null=True)
    phone_type = fields.IntField(default=1,null=True)

async def main():
    await Tortoise.init(db_url="sqlite://ab.db", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

#    stefan = Contact(first_name='Stefan', last_name='Kotarac', phone_number='123')
#    igor = Contact(first_name='Igor', last_name='Jeremic', phone_number='3123123')
    
#    await stefan.save()
#    await igor.save()

    
    for i in await Contact.filter(first_name='Stefan').all():
        print(i,i.first_name) 
    
    
if __name__=='__main__':

    run_async(main())

