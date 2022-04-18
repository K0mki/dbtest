from fastapi import FastAPI, Path, Query , HTTPException, status
from tortoise.contrib.fastapi import register_tortoise
from models import *

app = FastAPI()

db = []

@app.get("/")
async def index():
    return {'message': 'go to http://127.0.0.1:8000/docs for the API doc'}

@app.post('/create-contact')
async def create_contact(contact: ContactIn_Pydantic):
    return await Contact.create(**contact.dict(exclude_unset=True))


@app.get("/contacts") 
async def all_contacts():                                                                                
    return await Contact_Pydantic.from_queryset(Contact.all())
        

@app.get("/get-contact/{contact_id}")
async def get_contact(contact_id: str):                                                                           
    return await Contact_Pydantic.from_queryset_single(Contact.get(id=contact_id))

@app.put("/update-contact/{contact_id}",response_model=Contact_Pydantic,status_code=status.HTTP_200_OK)
async def update_contact(contact_id: str,update:ContactIn_Pydantic):
    contact = await Contact.get(id=contact_id)
    update = update.dict(exclude_unset=True)
    contact.first_name = update['first_name']
    contact.last_name = update['last_name']
    await contact.save()
    return await Contact_Pydantic.from_tortoise_orm(contact)

@app.delete('/delete-contact/{contact_id}')
async def delete_(contact_id: str):
    await Contact.filter(id=contact_id).delete()
    return{"Succes": "Item deleted"}


register_tortoise(
    app,
    db_url='postgres://stefan:123@localhost:5432/adr',
    modules={'models':['main']},
    generate_schemas=True
    )