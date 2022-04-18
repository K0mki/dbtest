from fastapi import FastAPI, Path, Query , HTTPException, status
from tortoise.contrib.fastapi import register_tortoise
from models import *

app = FastAPI()

db = []

@app.get("/")
async def index():
    return {'message': 'Hello'}

@app.post('/create-contact')
async def create_contact(contact: ContactIn_Pydantic):
    return await Contact.create(**contact.dict(exclude_unset=True))


@app.get("/contacts") 
async def all_contacts():                                                                                
    return await Contact_Pydantic.from_queryset(Contact.all())
        

@app.get("/get-contact/{contact_id}")
async def get_contact(contact_id: str):                                                                           
    return await Contact_Pydantic.from_queryset_single(Contact.get(id=contact_id))

# @app.put("/update-contact/{contact_id}",response_model=Contact_Pydantic,status_code=status.HTTP_200_OK)
# async def update_contact(contact_id: str,contact:Contact_Pydantic):

#     contact_to_update = Contact_Pydantic.filter(Contact.id==contact_id).first()
#     contact_to_update.first_name = contact.first_name
#     contact_to_update.last_name = contact.last_name
#     # contact = Contact_Pydantic.filter()
#     # if contact_id not in db:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact ID does not exist")
    
#     # if Contact.first_name != None:
#     #     db[contact_id].first_name = Contact.first_name

#     # if Contact.last_name != None:
#     #     db[contact_id].last_name = Contact.last_name

#     # return db[contact_id]    


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