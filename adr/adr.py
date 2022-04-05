#!.venv/bin/python
from enum import unique
import uuid
from tortoise import Tortoise, run_async, fields 
from tortoise.models import Model 
# import sys
# import argparse 


class PhoneType(Model):
    class Meta:
        table='lookup_phone_types'
    
    id = fields.UUIDField(pk=True)
    name = fields.CharField(8)

    # phones: fields.ReverseRelation["PhoneNumber"]                   # mislim da nije bitno, jer ti ne treba funkcionalnost daj mi sve mobilne telefone 

    # phones1 : fields.ReverseRelation["SearchList"]                  # ?!?


class Contact(Model):
    class Meta:
        table='contacts'

    id = fields.UUIDField(pk=True)
    first_name = fields.TextField()
    last_name = fields.TextField()

    # phone_numbers: fields.ReverseRelation["PhoneNumber"]

    # async def mk_search(self):

    #     sl = await SearchList.filter(contact=self).get_or_none()
    #     if not sl:
    #         sl = SearchList(contact=self)

    #     pn = await self.fetch_related('phone_numbers')
    #     def normalize_pn(n):
    #         for x in ('-',' ','/','(',')','+'):
    #             n=n.replace(x, '')
    #         return n

    #     search = [x for x in [first_name, last_name] if x] + [normalize_pn(x.phone_number)+(' '+x.note) if x.note else '' for x in self.phone_numbers]
    #     search = ' '.join(search).lower()

    #     if sl.search != search:
    #         sl.search = search
    #         await sl.save()


class PhoneNumber(Model):
    class Meta:
        table='phone_numbers'

    id = fields.UUIDField(pk = True)
    phone_number = fields.TextField()
    is_primary = fields.BooleanField(null = True, unique = True)                              # TODO: Obezbedi da jedan kontakt moze da ima samo jedan primarni telefon
    note = fields.TextField(null=True)

    contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact")

    phone_type : fields.ForeignKeyRelation[PhoneType] = fields.ForeignKeyField("models.PhoneType")

    #number : fields.ReverseRelation["SearchList"]                   # ?
    #primary : fields.ReverseRelation["SearchList"]                  # ?
    #type : fields.ReverseRelation["SearchList"]                     # ?
    #note1 : fields.ReverseRelation["SearchList"]                    # ?

class SearchList(Model):
    class Meta:
        table='search_list'

    id = fields.IntField(pk=True)
    contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact", unique=True)

    search: fields.TextField(null=True) 
    
    #id : fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact", related_name="id1", pk = True)
    #first_name : fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact", related_name="first", )
    #last_name : fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField("models.Contact", related_name="last")
    #phone_number : fields.ForeignKeyRelation[PhoneNumber] = fields.ForeignKeyField("models.PhoneNumber",related_name="number")
    #is_primary : fields.ForeignKeyRelation[PhoneNumber] = fields.ForeignKeyField("models.PhoneNumber",related_name="primary")
    #note : fields.ForeignKeyRelation[PhoneNumber] = fields.ForeignKeyField("models.PhoneNumber",related_name="note1")
    #phone_type_id : fields.ForeignKeyRelation[PhoneType] = fields.ForeignKeyField("models.PhoneType",related_name="type")

async def add_contact(first_name, last_name, phone_number, phone_type, is_primary, note):     #-a
    '''
        Add contact
    '''
    is_primary = 'true' if is_primary in (True, 1, 'True' , 'true' , 'yes' , 'da' , '1' ) else 'false'
    id   = uuid.uuid4()   # CONTACT ID
    # id_p = uuid.uuid4()   # PHONE ID

    c = Contact(id = id, first_name=first_name, last_name=last_name)
    await c.save()
    p = PhoneNumber (phone_number = phone_number , is_primary = is_primary , note = note , contact_id = id , phone_type_id = phone_type)
    await p.save()
    return await print('Added contact ID',(str(c.id)))

async def add_number(contact_id, phone_number, phone_type, is_primary, note):                 #-n
    '''
        Add another phone number to existing contact
    '''
    is_primary = True if is_primary in (True, 1, 'true','yes','da','1') else 'false'
    #id_p = uuid.uuid4()   # PHONE ID
    number = PhoneNumber (phone_number = phone_number , is_primary = is_primary , note = note , contact_id = contact_id , phone_type_id = phone_type)

    await number.save()

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

# async def ab():
#     '''
#         pytho3 ab.py [command] param1 param2 param3 ... [params zavise od komande]
#     '''

#     parser= argparse.ArgumentParser(description='Edit addressbook contacts')

#     parser.add_argument('-a', '--add',      metavar = ('[first_name]','[last_name]','[phone_number]','[phone_type]', '[is_primary]', '[note]'), help='Add a contact', nargs=6)
#     parser.add_argument('-n', '--number',   metavar = ('[contacts_id]','[phone_number]','[phone_type]','[is_primary]','[note]'), help='Add a phone to a contact', nargs=5)
#     parser.add_argument('-r', '--remove',   metavar = ('[id]'), help='Remove a contact by ID', nargs=1)
#     parser.add_argument('-u', '--update',   metavar = ('[id]', '[update]','[value]'), help='Update contact', nargs=3)
#     parser.add_argument('-s', '--search',   metavar = ('[first_name / last_name / phone/number / id]'), help='Search and print all contacts containing provided term', nargs=1)
#     # parser.add_argument('-d', '--details',  metavar = ('[id]'), help='Show details about contact with provided id', nargs=1)
#     # parser.add_argument('-l', '--list-all', metavar = (''), action='store_true', help='Show all contacts, sorted by provided arguments') # metavar=('[-o / -d]') ?

#     parser.add_argument('--sort',  help='Chose sorting parameter', default='first_name', choices=['first_name','last_name','phone_number','id'])
#     parser.add_argument('--direction', help='Chose sorting direction', default='asc', choices=['asc','desc'])

#     args=parser.parse_args()

#     if args.add:                #Add contact
#         add_contact(*args.add)
#         return True

#     if args.number:             #Add number
#         add_number(args.number[0],args.number[1],args.number[2],args.number[3],args.number[4])
#         return True

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
        
    # print('Unknow command')
    # return False
# run_async is a helper function to run simple async Tortoise scripts.

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
        
    # await remove_contact('first_name', 'Stefan')

    await add_contact('Stefan' , 'Kotarac' , '123456' , mobile, True , 'Moj telefon')
    
    # await add_number('5b52eee9-ea45-4815-b333-09f6ac79dd50','234567','Work','True','Drugi broj')

    # await update_contact('eb615da5-ec70-4a61-a35e-89be58accfc1','phone_number','2222222222')
   
    # await search_contacts('phone_number','2222222222')
  
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
    # if  not ab():
    #     sys.exit(1)
        
    # sys.exit(0)

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


