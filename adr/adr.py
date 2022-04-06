#!.venv/bin/python
import argparse
from dataclasses import field
from enum import unique
import sys
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

    phone_numbers: fields.ReverseRelation[PhoneNumber]

class PhoneNumber(Model):
    class Meta:
        table='phone_numbers'

    id = fields.UUIDField(pk = True)
    phone_number = fields.TextField()
    is_primary = fields.BooleanField(null = True, unique = True)                            
    note = fields.TextField(null=True)

    contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact",related_name="phone_numbers")

    phone_type : fields.ForeignKeyRelation[PhoneType] = fields.ForeignKeyField("models.PhoneType")

# class SearchList(Model):
#     class Meta:
#         table='search_list'

#     id : fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact", pk = True)
#     contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact", unique=True)

async def add_contact(first_name, last_name, phone_number, phone_type, is_primary, note):     #-a
    '''
        Add contact
    '''
    is_primary = 'true' if is_primary in (True, 1, 'True' , 'true' , 'yes' , 'da' , '1' ) else 'false'
    # id   = uuid.uuid4()   # CONTACT ID
    # id_p = uuid.uuid4()   # PHONE ID

    # stefan = Contact(first_name = 'Stefan', last_name = 'Kotarac')
    # await stefan.save()
    # phone  = PhoneNumber(phone_number = '123456', phone_type = mobile , is_primary= 'True', contact_id = stefan.id , note =  'Moj broj')
    # await phone.save()
    c = Contact ( first_name = first_name , last_name = last_name )
    await c.save()
    p = PhoneNumber ( phone_number = phone_number , is_primary = is_primary , note = note , contact_id = c.id , phone_type_id = phone_type )
    await p.save()
    return await print('Added contact ID', c.id)

async def add_c(first_name, last_name):     #-c
    '''
        Add only contact name
    '''    
    # await add_c(first_name="Boban", last_name="Rajovic")
    c = Contact ( first_name = first_name , last_name = last_name )
    await c.save()
    return print('Added contact ' , c.id)

async def add_number(contact_id, phone_number, phone_type, is_primary, note):                 #-n
    '''
        Add another phone number to existing contact
    '''
    is_primary = True if is_primary in (True, 1, 'true','yes','da','1') else 'false'
    #id_p = uuid.uuid4()   # PHONE ID
    number = PhoneNumber (phone_number = phone_number , is_primary = is_primary , note = note , contact_id = contact_id , phone_type_id = phone_type)
    await number.save()
    return await print('Added number ID', contact_id)

async def remove_contact(where,what):                                                                  #-n
    '''
        Remove contact connected to provided ID
    '''
    await Contact.filter(**{where:what}).delete()


async def update_contact(id, upd, value):                                                 #-u
    '''
        Update contact
    '''
    if upd in ('first_name','last_name'):
       contact = await Contact.filter(id = id).update(**{upd:value})
       contact.save()
    else:
       phone = await PhoneNumber.filter(id = id).update(**{upd:value})
       phone.save()

    return await print("Contact with ID %s updated!"%id)
async def search_contacts(search_term , what):                                                #-s
    '''
        Search for contacts by search_term, search term can be id, first_name, last_name or phone_number, then print it out
    '''
    # search_list = [(x.username, x.age) for x in await User.filter().all()]
    # return search_list
    
    if search_term in ('first_name','last_name'):
       contact =  await Contact.filter(**{search_term:what}).all()
       return await contact
    else:
       phone = await PhoneNumber.filter(**{search_term:what}).all()
       return await phone

# async def detailed_contact(id):                                                               #-d
#     '''
#         Show info for provided ID's contact
#     '''
    

# async def all_contacts(order_by, direction):                                                  #-l
#     '''
#         Return all contact ordered by order_by (id,fist_name,last_name,phone_number)
#     '''    
#     all = await Contact.all(), PhoneNumbers.all() #??
#     for a in all:
#         await print(f"{a[0]:<35} | {a[1]+' '+a[2]:^25} | {a[3]:<12} {a[4]:<6} {a[5]:>5} | {[6]}")

async def ab():
    '''
        pytho3 ab.py [command] param1 param2 param3 ... [params zavise od komande]
    '''

    parser = argparse.ArgumentParser(description='Edit addressbook contacts')

    parser.add_argument('-a', '--add',      metavar = ('[first_name]','[last_name]','[phone_number]','[phone_type]', '[is_primary]', '[note]'), help='Add a contact', nargs=6)
    parser.add_argument('-c', '--contact',  metavar = ('[first_name]','[last_name]'), help='Add only contact name', nargs=2)
    parser.add_argument('-n', '--number',   metavar = ('[contacts_id]','[phone_number]','[phone_type]','[is_primary]','[note]'), help='Add a phone to a contact', nargs=5)
#     parser.add_argument('-r', '--remove',   metavar = ('[id]'), help='Remove a contact by ID', nargs=1)
#     parser.add_argument('-u', '--update',   metavar = ('[id]', '[update]','[value]'), help='Update contact', nargs=3)
#     parser.add_argument('-s', '--search',   metavar = ('[first_name / last_name / phone/number / id]'), help='Search and print all contacts containing provided term', nargs=1)
#     parser.add_argument('-d', '--details',  metavar = ('[id]'), help='Show details about contact with provided id', nargs=1)
#     parser.add_argument('-l', '--list-all', metavar = (''), action='store_true', help='Show all contacts, sorted by provided arguments') # metavar=('[-o / -d]') ?

#     parser.add_argument('--sort',  help='Chose sorting parameter', default='first_name', choices=['first_name','last_name','phone_number','id'])
#     parser.add_argument('--direction', help='Chose sorting direction', default='asc', choices=['asc','desc'])

    args = parser.parse_args()

    if args.add:                #Add contact
        await add_contact(*args.add)
        return await True

    if args.contact:                #Add only contact name
        await add_c(args.c[0],args.c[1])
        return await True

    if args.number:             #Add number
        await add_number(args.number[0],args.number[1],args.number[2],args.number[3],args.number[4])
        return await True

#     if args.remove:             #Remove contact 
#         remove_contact(args.remove[0])    
#         return True
    
#     if args.update:             #Update contact
#         update_contact(*args.update)
#         return True

#     if args.search:             #Search contact
#         search_contacts(*args.search, args.sort, args.direction)
#         return True

    # if args.details:            #Search specific user
    #     detailed_contact(args.details[0])
    #     return True

    # if args.list_all:           #List contacts
    #     try:
    #         all_contacts(args.sort, args.direction)
    #     except Exception as e:
    #         print('Greska')
    #         return False
        
    #     return True
        
    print('Unknow command')
    return False

async def run():
    # await Tortoise.init(db_url="sqlite://adr.sql",modules={"models": ["__main__"]})  #postgres://stefan:123@localhost:5432/adr.sql
    await Tortoise.init(db_url="postgres://stefan:123@localhost:5432/adr" ,modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    mobile = await PhoneType.filter(name='Mobile').get_or_none()
    if not mobile:
        mobile = PhoneType(name="Mobile")
        await mobile.save()    
    work = await PhoneType.filter(name='Work').get_or_none()
    if not work:
        work = PhoneType(name="Work")
        await work.save()
    home = await PhoneType.filter(name='Home').get_or_none()
    if not home:        
        home = PhoneType(name="Home")
        await home.save()  
    other = await PhoneType.filter(name='Other').get_or_none()
    if not other:          
        other = PhoneType(name="Other")
        await other.save()
        
    # stefan = Contact(first_name = 'Stefan', last_name = 'Kotarac')
    # await stefan.save()
    # phone  = PhoneNumber(phone_number = '123456', phone_type = mobile , is_primary= 'True', contact_id = stefan.id , note =  'Moj broj')
    # await phone.save()

    # await remove_contact('first_name', 'Stefan')

    # stefan = Contact(first_name = 'Stefan', last_name = 'Kotarac')
    # await stefan.save()
    # phone  = PhoneNumber(phone_number = '123456', phone_type = mobile , is_primary= 'True', contact_id = stefan.id , note =  'Moj broj')
    # await phone.save()
    # await add_contact('Stefan' , 'Kotarac' , '123456' , mobile, 'True' , 'Moj telefon')
    
    # await add_number('bc1fa5ff-20c1-43a2-88c5-f82386534a46','234567','Work','True','Drugi broj')

    # await add_c(first_name="Boban", last_name="Rajovic")

    # await update_contact('eb615da5-ec70-4a61-a35e-89be58accfc1','phone_number','2222222222')
   
    # await search_contacts('phone_number','2222222222')
    
    if not await ab():
        await sys.exit(1)
        
    await sys.exit(0)
  
async def run2():
    await Tortoise.init(db_url="sqlite://adr.db",modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()



    igors = [x for x in await Contact.filter(first_name='Igor').limit(1).all()]
    if igors:
        igor=igors[0]
        
        await igor.fetch_related('phone_numbers')
        for pn in igor.phone_numbers:
            print('pn',pn.phone_number)
        
        # igor.phone_numbers.append(PhoneNumber(phone_number='11231323131',is_primary=True, note='asdaasdad',phone_type=main))


    '''


    else:
        igor = Contact(first_name='Igor',last_name='Jeremic')
        await igor.save()

    igor_main_phone = PhoneNumbers(phone_number='123131',is_primary=True, note='asda',contact=igor,phone_type=main)
    await igor_main_phone.save()

    '''
    '''
    main = PhoneTypes(phone_types="Main")
    await main.save()
    work = PhoneTypes(phone_types="Work")
    await work.save()
    home = PhoneTypes(phone_types="Home")
    await home.save()    
    other = PhoneTypes(phone_types="Other")
    await other.save()

    await add_contact('Stefan','Kotarac','123456',main,True,'Moj broj')
    '''

if __name__ == "__main__":

    run_async(run())


