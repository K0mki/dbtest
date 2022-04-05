import uuid
from models import *

async def add_contact(first_name, last_name, phone_number, phone_type, is_primary, note):     #-a
    '''
        Add contact
    '''
    is_primary = 'true' if is_primary in (True, 1, 'True' , 'true' , 'yes' , 'da' , '1' ) else 'false'
    id   = uuid.uuid4()   # CONTACT ID
    # id_p = uuid.uuid4()   # PHONE ID

    if phone_type in ('Main','Work','Home','Other'):
        c = Contact(id = id, first_name=first_name, last_name=last_name)
        await c.save()
        p = PhoneNumber (phone_number = phone_number , is_primary = is_primary , note = note , contact_id = id , phone_type_id = phone_type)
        await p.save()
    else: await print('Error: phone_type must be: Main , Work , Home or Other !')
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