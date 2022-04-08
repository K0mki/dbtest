import argparse
import sys
from tortoise import Tortoise
from models import * 

async def create():
    await Tortoise.init(db_url="postgres://stefan:123@localhost:5432/adr" , modules={"models": ["__main__"]})
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

    if not await arg():
        await sys.exit(1)

    await sys.exit(0)

async def add_contact(first_name, last_name, phone_number, p_type, is_primary, note):                   #-a
    '''
        Add contact
    '''
    is_primary =  is_primary in (True, 1, 'True' , 'true' , 'yes' , 'da' , '1' )
    note = '' if note in ('',' ') else note

    contact = Contact( first_name = first_name , last_name = last_name)  
    await contact.save()
    phone = PhoneNumber( phone_number = phone_number , phone_type = p_type , is_primary = is_primary , contact_id = contact.id ,note = note)
    await phone.save()

    return await print('Added contact ID')

async def add_number(contact_id, phone_number, p_type, is_primary, note):                               #-n
    '''
        Add another phone number to existing contact
    '''
    is_primary =  is_primary in (True, 1, 'True' , 'true' , 'yes' , 'da' , '1' )
    note = '' if note in ('',' ') else note

    phone = PhoneNumber( phone_number = phone_number , phone_type = p_type , is_primary = is_primary , contact_id = contact_id ,note = note)
    await phone.save()
    return await print('Added number ID')

async def remove_contact(where,what):                                                                    #-n
    '''
        Remove contact
    '''
    await Contact.filter(**{where:what}).delete()
    return await print("Removed contact" )

async def update_contact(id, upd, value):                                                                #-u
    '''
        Update contact
    '''
    contact = await Contact.filter(id=id).prefetch_related('phone_numbers','phone_numbers__phone_type').get_or_none()

    await contact.save()

# async def search_contacts(search_term , what):                                                #-s
#     '''
#         Search for contacts by search_term, search term can be id, first_name, last_name or phone_number, then print it out
#     '''
#     # search_list = [(x.username, x.age) for x in await User.filter().all()]
#     # return search_list
    
#     if search_term in ('first_name','last_name'):
#        contact =  await Contact.filter(**{search_term:what}).all()
#        return await contact
#     else:
#        phone = await PhoneNumber.filter(**{search_term:what}).all()
#        return await phone

# async def detailed_contact(id):                                                               #-d
#     '''
#         Show info for provided ID's contact
#     '''

# async def all_contacts(order_by, direction):                                                           #-l
#     '''
#         Return all contact ordered by order_by (id,fist_name,last_name,phone_number)
#     '''    
#     all = await SearchList
#     for a in all:
#         await print(f"{a[0]:<35} | {a[1]+' '+a[2]:^25} | {a[3]:<12} {a[4]:<6} {a[5]:>5} | {[6]}")

async def arg():
    '''
        python3 adr.py [command] param1 param2 param3 ... [params zavise od komande]
    '''

    parser = argparse.ArgumentParser(description='Edit addressbook contacts')

    parser.add_argument('-a', '--add',      metavar = ('[first_name]','[last_name]','[phone_number]','[phone_type]', '[is_primary]', '[note]'), help='Add a contact', nargs=6)
    parser.add_argument('-n', '--number',   metavar = ('[contacts_id]','[phone_number]','[phone_type]','[is_primary]','[note]'), help='Add aother phone number to a contact', nargs=5)
    parser.add_argument('-r', '--remove',   metavar = ('[what]' , '[where]'), help='Remove a contact', nargs=2)
    # parser.add_argument('-u', '--update',   metavar = ('[id]', '[update]','[value]'), help='Update contact', nargs=3)
    # parser.add_argument('-l', '--list-all', metavar = (''), action='store_true', help='Show all contacts, sorted by provided arguments')
    # parser.add_argument('-s', '--search',   metavar = ('[first_name / last_name / phone/number / id]'), help='Search and print all contacts containing provided term', nargs=1)
    # parser.add_argument('-d', '--details',  metavar = ('[id]'), help='Show details about contact with provided id', nargs=1)

    # parser.add_argument('--sort',  help='Chose sorting parameter', default='first_name', choices=['first_name','last_name','phone_number','id'])
    # parser.add_argument('--direction', help='Chose sorting direction', default='asc', choices=['asc','desc'])


    args = parser.parse_args()

    if args.add:                #Add contact
        await add_contact(*args.add)
        return True

    if args.number:             #Add number
        await add_number(*args.number)
        return True

    if args.remove:             #Remove contact 
        await remove_contact(*args.remove)    
        return True

    # if args.update:             #Update contact
    #     update_contact(*args.update)
    #     return True

    # if args.search:             #Search contact
    #     search_contacts(*args.search, args.sort, args.direction)
    #     return True

    # if args.details:            #Search specific user
    #     detailed_contact(args.details[0])
    #     return True

    # if args.list_all:           #List contacts
    #     try:
    #         await all_contacts(args.sort, args.direction)
    #     except Exception as e:
    #         await print('Greska')
    #         return False
        
    #     return True

    print('Unknow command')
    return False
